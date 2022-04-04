# variables ##################################################################

DIST_PATH = release

version = $(shell ./presentation.py --version)
VERSION = $(lastword $(version))
IDENTIFIER = $(word 2,$(version))


# targets ####################################################################

# note: for pkgutil to work, the é should be UTF-8 NFD encoded
# this could be forced using this line in pkg build rule, but it would add a dependency
# convmv -r -f utf8 -t utf8 --nfd --notest $(DIST_PATH)

app     := Présentation.app
script  := presentation.py
icon    := presentation.icns
iconset := presentation.iconset
venv    := env
dist    := osx-presentation-$(VERSION).pkg
src     := osx-presentation-$(VERSION).tbz


# rules ######################################################################

.PHONY: all clean dev pkg archive

all: $(app)

$(app): $(script) $(icon) $(venv) makefile
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
	cp $< $@/Contents/MacOS/
	
	mkdir -p $@/Contents/Resources/
	cp $(icon) $@/Contents/Resources/
	
	cp -R $(venv)/lib/python3.8/site-packages $@/Contents/Resources/packages
	
	echo "\
	<?xml version="1.0" encoding='UTF-8'?> \
	<!DOCTYPE plist PUBLIC '-//Apple//DTD PLIST 1.0//EN' 'http://www.apple.com/DTDs/PropertyList-1.0.dtd'> \
	<plist version='1.0'> \
	<dict> \
		<key>com.apple.security.device.camera</key> \
		<true/> \
	</dict> \
	</plist>" | plutil -convert xml1 - -o $@/Contents/Entitlements.plist
	codesign --verbose=4 --force --deep -s "Developer ID Application: Renaud Blanch (J6M3684Y6M)"  --entitlements $@/Contents/Entitlements.plist $@
	
	touch $@

$(icon): $(iconset)
	iconutil --convert icns --output $@ $<

$(iconset): $(script)
	mkdir -p $@
	./$< --icon > $@/icon_256x256.png

$(venv):
	/usr/bin/python3 -m venv $@
	$@/bin/pip install --upgrade pip
	$@/bin/pip install --platform macosx_10_9_x86_64 --only-binary=:all: --target=$@/lib/python3.8/site-packages -r requirements.txt

dev: $(dev)

$(dev): $(app)
	cp -R $< $@
	rm $@/Contents/MacOS/$(script)
	ln $(script) $@/Contents/MacOS/

archive:
	hg archive -r $(VERSION) -t tbz2 $@

pkg: $(dist)

$(dist): $(app)
	mkdir -p $(DIST_PATH)
	cp -r $^ $(DIST_PATH)
	pkgbuild --root $(DIST_PATH) --identifier $(IDENTIFIER) --version $(VERSION) --install-location /Applications temp.pkg
	productsign --sign "Developer ID Installer: Renaud Blanch (J6M3684Y6M)" temp.pkg $@
	rm temp.pkg
	rm -rf $(DIST_PATH)


clean:
	-rm -rf $(app) $(src) $(dist) $(icon) $(iconset) $(venv) $(dev) $(DIST_PATH)
