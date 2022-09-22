# variables ##################################################################

version = $(shell ./presentation.py --version)
VERSION = $(lastword $(version))
IDENTIFIER = $(word 2,$(version))


# targets ####################################################################

# note: for pkgutil to work, the é should be UTF-8 NFD encoded
# this could be forced using this line in pkg build rule, but it would add a dependency
# convmv -r -f utf8 -t utf8 --nfd --notest $(DIST_PATH)

app     := Présentation.app
dev     := Dev.app
script  := presentation.py
icon    := presentation.icns
iconset := presentation.iconset
objc    := packages
venv    := env
dist    := osx-presentation-$(VERSION).pkg


# rules ######################################################################

.PHONY: all dev pkg staple archive clean

all: $(app)

$(app): $(dev)
	rm -rf $@
	
	cp -RL $< $@
	cp -Rf $(objc) $@/Contents/Resources/packages
	
	echo "\
	<?xml version="1.0" encoding='UTF-8'?> \
	<!DOCTYPE plist PUBLIC '-//Apple//DTD PLIST 1.0//EN' 'http://www.apple.com/DTDs/PropertyList-1.0.dtd'> \
	<plist version='1.0'> \
	<dict> \
		<key>com.apple.security.device.camera</key> \
		<true/> \
		<key>com.apple.security.cs.allow-unsigned-executable-memory</key> \
		<true/> \
	</dict> \
	</plist>" | plutil -convert xml1 - -o $@/Contents/Entitlements.plist
	find $@ -name '*.so' -exec codesign --verbose --force --timestamp -s "Developer ID Application: Renaud Blanch (J6M3684Y6M)" --entitlements $@/Contents/Entitlements.plist -o runtime {} ';'
	codesign --verbose --force --deep --timestamp -s "Developer ID Application: Renaud Blanch (J6M3684Y6M)" --entitlements $@/Contents/Entitlements.plist -o runtime $@
	
	touch $@


dev: $(dev)

$(dev): $(script) $(icon) $(objc) makefile
	mkdir -p $@/Contents/
	echo "APPL????" > $@/Contents/PkgInfo
	echo "\
	<?xml version='1.0' encoding='UTF-8'?> \
	<!DOCTYPE plist PUBLIC '-//Apple//DTD PLIST 1.0//EN' 'http://www.apple.com/DTDs/PropertyList-1.0.dtd'> \
	<plist version='1.0'> \
	<dict> \
		<key>CFBundleExecutable</key><string>$<</string> \
		<key>CFBundleIdentifier</key><string>$(IDENTIFIER)</string> \
		<key>CFBundleDocumentTypes</key><array><dict> \
			<key>CFBundleTypeName</key><string>Adobe PDF document</string> \
			<key>LSItemContentTypes</key><array> \
				<string>com.adobe.pdf</string> \
			</array> \
			<key>CFBundleTypeRole</key><string>Viewer</string> \
			<key>LSHandlerRank</key><string>Alternate</string> \
		</dict></array> \
		<key>CFBundleShortVersionString</key><string>$(VERSION)</string> \
		<key>NSHumanReadableCopyright</key><string>Copyright © 2011-2022 Renaud Blanch</string> \
		<key>CFBundleIconFile</key><string>presentation</string> \
		<key>NSCameraUsageDescription</key><string>This app requires camera access to display video feed</string> \
	</dict> \
	</plist>" > $@/Contents/Info.plist
	
	mkdir -p $@/Contents/MacOS/
	ln -f $< $@/Contents/MacOS/
	
	mkdir -p $@/Contents/Resources/
	ln -f $(icon) $@/Contents/Resources/
	
	touch $@


$(icon): $(iconset)
	iconutil --convert icns --output $@ $<

$(iconset): $(script)
	mkdir -p $@
	./$< --icon > $@/icon_256x256.png
	touch $@


$(objc): requirements.txt $(venv)
	for python_version in 3.7 3.8 3.9; do \
		mkdir -p $@/$$python_version; \
		$(venv)/bin/pip install --platform macosx_10_9_x86_64 --only-binary=:all: --upgrade --python-version=$$python_version --target=$@/$$python_version -r $< ; \
	done
#	$(venv)/bin/pip install --platform macosx_10_9_x86_64 --only-binary=:all: --upgrade --target=$@ -r $<
#	$(venv)/bin/pip install --platform macosx_10_9_universal2 --only-binary=:all: --target=$@ -r $<
	
$(venv):
	/usr/bin/python3 -m venv $@
	$@/bin/pip install --upgrade pip
	touch $@

pkg: $(dist)
	xcrun altool --notarize-app --primary-bundle-id $(IDENTIFIER) --username 'blanch@imag.fr' --password '@keychain:Developer-altool' --file $<

$(dist): $(app)
	productbuild --timestamp --sign "Developer ID Installer: Renaud Blanch (J6M3684Y6M)" --identifier $(IDENTIFIER) --version $(VERSION) --component $^ /Applications $@


staple:
	xcrun stapler staple $(dist)


archive:
	hg archive -r $(VERSION) -t tbz2 $@


clean:
	-rm -rf  $(dist) $(app) $(dev) $(icon) $(iconset) $(objc) $(venv)
