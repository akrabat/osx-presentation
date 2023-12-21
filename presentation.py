#! /usr/bin/python3
# -*- coding: utf-8 -*-


"""
A PDF presentation tool for Mac OS X

Copyright (c) 2011--2022, IIHM/LIG - Renaud Blanch <http://iihm.imag.fr/blanch/>
Licence: GPLv3 or higher <http://www.gnu.org/licenses/gpl.html>
"""


# imports ###################################################################

import sys
import os
import time
import getopt
import textwrap
import mimetypes
import base64
import tempfile

from math import exp, hypot
from collections import defaultdict


# constants and helpers #####################################################

NAME = "Présentation"
ID = "fr.imag.iihm.blanch.osx-presentation"
MAJOR, MINOR, PATCH, BETA = 3, 2, 2, ''
VERSION = "%s.%s.%s%s" % (MAJOR, MINOR, PATCH, BETA)
HOME = "http://iihm.imag.fr/blanch/software/osx-presentation/"
COPYRIGHT = "Copyright © 2011-2022 Renaud Blanch"
CREDITS = """
Home: <a href='%s'>osx-presentation</a> <br/>
Source: <a href='https://foss.heptapod.net/macos-apps/osx-presentation/blob/%s/presentation.py'>presentation.py</a> <br/>
Licence: <a href='http://www.gnu.org/licenses/gpl-3.0.txt'>GPLv3</a>+ <br/>
Built on the shoulders of <a href="https://pyobjc.readthedocs.io">PyObjC</a>.  <br/>
Icon courtesy of <a href="http://www.dlanham.com/">David Lanham</a>. <br/><br/>
<a href='https://www.buymeacoffee.com/rndblnch'><b>Buy me a Tea</b></a>! <br/>
""" % (HOME, VERSION)

ICON = base64.b64decode(b'iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAABGaElEQVR42u2dd3hU1fb3AyqCiILYaDYE6/UqzS6oVEGwooSiIEWFUKSXgIgoTSxICyC9JHRCC5AEQkivpDfS26SA/n73ve/713n3OrNOsudkyp6Zc2bOmdnzPN/neqnDzPl899prrb22jyAIPpbEX/zlQa9mZtQcJf9x3b+scW3CODcA/vJw2CXIb0PdTnSHGd1O/ZrmejcDbgD85a0ruznYWxC1JGpFdBeqNdHdqNb4Y/Dzd+Kvv13PZsANgL+8GfY7KdgB8HuI2hLdN3369CeuXo0cfuVKxIicnNzF8fEJYyMirg4/ffpMX/Lz7fHXtcHf25IyA10ZATcA/vLEUN4S7C3NwU70QFhY+AeZmVlLSkpKD9XW1pXcuvW3YEn19TdvVVRUnk1Nve5Hfu/9+OfcTRkBHRFwA+Av/nIj7K1xpb4XYb//+PETbwPspaVlhwyGmjRrsNsSmEFGRqY/+XMfRCNojX//7XowAW4A/KUn2M0BbxX2EydOvJ2SkupXWFgUUFVVfc0Z2K2putqQfuDAwf64PWiD7+kOfK/NuAHwF385DzudpKNhbwewb9q0qWdMTOwXubl569SEXa6bqDoSDcTGxc8i7+UhfF+ttG4C3AD4Sy+w0/v29lu3bn0pNjbui7y8vLUAO4TirgJeDr5cUdHRs8l7fBjfq2QCmtwOcAPgL1fC3swR2L/9dmpXSNLl5eWvheSbrSSdO+GXdPjwkVHkvXfASKClVnMC3AD4yx2wWyq/wf5Zysj7awV2e8CXVFtX//f7w4e/iNuBe6jEIDcA/vLYUN7ejPwDly9fHiGV35zNyGsFfkk5uXnHyb/xcfh3otG10FoUwA2Av5zdtzOX31yVkXc3+LSmT58xgPzbu2CishW1FeAGwF8emZEXYd+4ETLyMV/oDXaxtl+SKNRmnRJqEjcL1VeXCFXnxwtVF78VDLHrhdq8i3YZQGZW1knyeXTHpGAbNEnNVAW4AfCXMxl5WNXab96ypQdk5KXymzsy8g7DXp4p1BGoa1N3CYaolUJVyHijzjdVJegc+e+IxUJ91Q0mA6iprfuHfEaQC3gUzbGVlnIB3AB4ks6+jPxUkpEPv/xBXn7B2opKkqSrqy/RTShfXSjUFUY2wF4twc4AfeW5L01UdYWYQG2lZfhv3mrQ3r1755DP7ilMCNK5AG4A/KXtjHw4gT1fhL3KCPvf/wgN0gPsGYGCIZrAHvqtCLwz0IMqzjaqOn6TTfhBJDoKIp/lC5gLaIsGq4ltADcAnpGnMvJXRmRlZYs98jU1tWl/07DLpSXYa6uM+3YCe03ceqH68myh+sIEAvsExaE30ZkvTKMAGfiSSDmzkny+fYi6+hgPD92llW0ANwCvzciffBtOsxUVFQdIsMulVfAB9jqE3SDBLskF0IPKUTUFV63CL2n+/PlfkM/9GSoZqIltADcAL8jIQ4+8BDs5tHLNHOw2wXcT/CLs2aeE2qTNQk3kElPY3QR9g05/IVTFbbQJP4jMEdhAvot/a20bwA3AwzLyW0hGPi4OeuTz1wHs5OG7ZQt4raz69RUkI59PMvLXd4mwGwjcBnPAuxl6WhUXZzEZAGl0yiPfT2+iJ7S0DeAGoOOM/FSSkZeSdJUkI28v7O5c9cUknQj7bqEm5ifBcHGCUTqAvkzUOKOCxwm1pelMJtCrV+9BsmrAHe7eBnAD0ElG3hT2qrN1JCPvKOyuXvUB9nqSka/LCDLCHja1EXidQk+rKnEHkwEEBgb9RL7LfxF1xi2a25uCuAHoKCOvtNQAX8zIl5J9e2aQUJvwq1ATDrB/hfIc6EGloFPjhPLQhUwGQM48XCXfbS8f4/kATTQFcQNwP+wNGfmysnLVYFcr3DeBPWKOUHPpKwp4z4W+UWNF1VUWMJkA+b5f8zG2Bj+Iz8Id3AA8K0nHXH5jychradUXYc8hGfnkLULNNX8Rdkmugf5LTUEv6uRYoYSoOu04kwFs3759IXkOnifq5NN4TNhtJwS5AahTfsMRVZt7GqfWOJaRd+eqf5Nk5OvzLwl1KQT2KFPYOfRG6GlVRK5hMoDk5JRz5Nno4dN4NsCt5UBuAApm5KWpNe6G3d5VvwH2tN1CbezPQk3oV2aB59Cb0Qmjik+MEeprKmwaAHYFvkL0pI9xTkBrd+YBvNEANJ2RVxv8m4Yiob7omlBP9u11BPbay9OMwHPoHYKeliHvClMUMHfu3PHkOXrWxzgyzK1dgd5gAE5fGgGwq52RVwP+m3XVws2yJKE+67BQF2eEvTZ0oigOvTLQFx9vVEX0BiYDIJOLD/sYjwg/gttFt20DPM0AFMjIn3gbYC8r0w/sIvA07Im/CbWRcxtg1wL0lR4KPagIVXxqEpMBFBeXQFfgyz4aOBykZwPQfUbeKeAJ7Ddzg4X61K1CXfRSoTZsolEuhL6KQy8UHQONblDNjTgmE/D19f2EPINP+7j5cJBeDEDxjLyuYK/MEm7mnW4KO4deE9BLKiSqiNvOZABnzpz9w6dxRoDbugK1aACKZOTxQIzmMvJMsN8IFerT9wj18auEOgJ4nRx4Dr2moC882qjiM35MBkDuE4SuwN7YFdjeXV2BWjAAr8jIm4WdZORvFl8TbmYfNsIePoloIodeZ9A3ylcoPOIr1FWwdQX26dNnIHYF0oeDvMIA5MA7lJHXFewkSXeLhj3CD4H3dOi/8Arob1CqTD3G2hW4yN1dga42ADn4d1Cre5Mk3ZUrESP0mpEXk3QAe/LvQv21eRTsHHpPhL5Bh32F4vPz7O0KfMxdXYGuNAAafGkP3xqd776AgICXrl9P029GniTpbl7fKtRHzRPqm8CufegNCZuE2oIIMv/+Gw69A9BLKhA1SqgzWO4KrEcZamr+hzz7rxJ1c1dXoKsMoJlsxYd/aFs/P7+upAw3vbZWR6t7WXIj7LHLhPrLk4zSIvQhqLAZlld6AjyAT2b5i4LhFpUXvuHQOwC9qCCjqjLOWYVf0tq166a5sytQbQNoRsHfAkN9WPEfIOHPdK3v4W9VZQm3CkOFmxl7hfqEVY2w24I+TAPQI+jVkd8LNemHBEPiJjLLfr5JeF997UdxpZLgNzWBrzn0dkJPqyR8lVXwJUUbuwJfcldXoJoGIA/5YdVvN2HCV93LyyvOaw72miLhVkmUcDNzr3AzcTUBfHJT4HUCfYMI8DVph0xkSN5JrrsippB5ogn4chOoCPmaQ28H9PmgQKMKjk6wCT+o3Hg4yG1dgWobwG0Y8kM2v/2YMWOeITfApmsF9ls5R0TYb0ZOF+qvTPYM6KXwPnS6YEjd28QAarLPCHVVxVbhl5sAM/TB3g29UZ83qCrnslX4JY0aJXYFumVkuFoGQIf9AP/9o0aNetZgMGS4HPZ6kpEvTzbCnvK7cDN6vnCTwA7yGOjlh21CJpGQP6AJ/LVF8Uzgy02g/PzXHHpG6PMONaok4ncmAzAzMtxlXYFqGIAU+kthP3Q5dSHnoKNdAjzAnn+6CeweDz1VsoOMvgn8JNyHkVX2wm9iAue+1jb0R9WDPt8O6GkVnJjKZADFpiPD27tyG6CGATTHN98KkxqdSXnvdzVhv5UWINyM+164GTG5CfDeAr2Ura+O+cV01ScZ/rpag8PwN5pAmlB2bkpT6E9x6E100Kjcg5+JMhSnMZlAr97uGRmutAHQ+37I9neYP39BP/IA/a1URv4WSdLdgn07wC7Jy6Gnb6wVE33XidKPCLXl2U6Db2ICJcQEzk7h0NuAnlZZ3F4mA3DXyHClDaA5OldrzGg+Tu6MP+5Qkg5gzyKwJ60WbhHIb9HAc+ibKvQ7I/hENTkhiqz65lRDTKD0zBQT6Es49KY60KiC4NlMBpBhHBne08fFI8OVNAB69QcH6zRgwMCX7Vn9xcx8zAIC+xQOvT1tuBf9hOqUvSL8tcXJqoDf1AQmuwf6I9qHPofW/s+EmvJ8mwZQbRC7Al0+MlxpA7gdExiw+j9x7tx5f2b407dx6B3pvT83UahOCBAMWezlPaVMoOT0ZA69Behz9o9sUEXaWaYoYPv2HTAy/DmijriFVr0cqKQBSJn/NtjW+Aw58xzMBD9k7Zmgn8Shl3XkVcdvJFNoolwGftNI4FsOvRnoQdmgfSOFwos/MRlAVHSM1BX4qKu6ApUyACn8b4l1TKhn/pt0/OWw1OmhEUdv0Fe7EXqpI68q5jenynuKJAZJ1FF+bb1QHDzJM6E/4Bj0ctVCyzVbVyA9Mlz1cqCSBiCV/tpjPbM30+oPvfYagd6gA+jLafhVSvQ5YgJVKUFGIzg7XRnoD+sfelF7PxWyiCqywpmigHnz5n/pysNBShqAlP1/EBMZrzMZAOnQ49DbceCGdOXV5EdoAny5CVQSE6hM2i+UR/1BjMDPg6Af6RD0tArDf7VtAORzDAsL24kjw6WuQFW3AUoZgFT+uxv7maGvuS+LAYhDMzj0TAduKiNWCLUVBZqD39QEAkUTEI3g2h/ijDxvhV7UHqOyD46zCr4kMg8DugL7uOpwkJIG0AIzlx1xzNE7dhkAh97qgRtD+gnNgm/RBBKNKiNGUHR6mrah36889KDMBn0iVBddtwq/JF/f0R9TI8PvVnMboKQBSN1/nbCj6V3S/19tcwtA5uRx6C2dshsnVIQtFHvx9QC/iQkkBwoVBH5a5THbxHFZ3gR95u5GFV3dYhV8SYcOBf6MI8NV7wpUywDgzfcnXYBpLOO0OPSm0EsHbqoSd+gKfBMTqCwWKsyYQEXiPqGMGEHRubleAT0oA5UdNIXps8OR4b1cMTJc1QiAXMQRxjIam0NvOkCj/MJMoaYwTrfwNzWBfUYlmKosOkAoOjvXo6HP2GUqQ1ke02fXu7drRoarmgM4c+ZMIEsegEPfqMpra8mYrnLdw29iAkmHGqAvN6NSYgSFYASHx3gk9Bm7PhaVvvNjoSQ+iOlz27bNNSPDla4CSF2AUMfsR044/cVkAIy31noq9KLIKTu4XtpTwDc1gSLRBMotGEB5vFFlsTuFopClQl7QGJdBn2UD+kwFoKeVe2oR02eWlJTskpHhapQBH8IM5luLFi1mOgsAV1d7I/TSAI2KKz+Q8l6+R8JPm0A5bQLxllUWs1MoDPEX8gLHeAT0JvrrY6G22naEZzC4ZmS4qo1AS5b4L2aKABJ+9TroJVWnHfdo8JuYQOIhy+DH7zVRacxfQuF5fyH30GjdQ58m6iNRpSmnmT6vOXPmjle7K1DpVmDpJOCT2NP8AYsB1GcGeRX0cIa+PHSheJjGW+C3ZAJy6GGAhlyl0cQILiwXcoO+tAP6TzUFfYN2fCQUXFzH9FlFGw8HvajmyHA1zwJAN9P7TFsAMAAvgF5SZcJ2rwPfnAlYg96ciq/+qVvoJV0nSt8zmulzwq5AVUeGq3EasB0mLmC6yXvZ2Tk2JwHfLE1SFvpz2oMeVBYywyPKe0qZQFnCQWb4S4lyD0/ULfQN2g76UChPD2X6nHx91R0ZrrQB3IkHGB7Bc82DcnJy01kMwFOhlyblVESu8ajynitMAKAvjTWq4OwS3UNP60b4JqbPCEeGv4CHgxTvClR6IIg0DqwzvukBYWHhZ1i2AVqCvkwh6EWRqTmG3CsceGvbgZSTZqGXVBTxp0dAnwraZlT6/olMn09eXn4yjgxXpStQjYlADjUDqQ19uZrQWxiKWX55uceX95RQXY1BNAE5+KWxe0TlBH3lEdDLVXUjlbErsPdAtUaGK20A9JFgKF/0Xbdu3SomA7i6xH7oz2oPemlGXpUXlfcUM4Hkkw3QSyo4u9ijoE8J+KBBRbGBtj8XItJQtxLb6+muQEW2AUoPBZV6AR5Cx3pj8eIlS1gMwBC1UvfQl5CZeGUXF3hleU85EzjRAH/RlQ0eBz2tjEA/q+BLSjR2BfakugIV2waoNRX4Aexgem3o0KGTWAygJmWXbqGXBmJWxG/nICtlAjEk9A/8yuOgT9lqVDLKUJpnFX5QVbVBGhneTemR4WqOBe+KNcwRTN2A6YHah/5EU+hBJefITbw3eHlPSRMoIQbgqdAbNUJUSVKwRfBpkZHhC9QYGa7GxSAtMUx5HM80DyPTgQ02m4HyLuoKemkEdvnV1by8p5IKw9Z7JPTJWxqVfWq5TfhB16KiVRkZrpYBtMM3CqeZhpBmIJu9APUlibqBXhQZg13Ny3uqqyhis8dBn0Rr8wib8IPKyMxwNUaGK303IH01WBfsYx6Ymno91qYBlGdqH3pUWdj3vLznQpWRwzOZ+8Z6FPS0Sq9fYjKBufPmfYldgYodDlLjctAW8slApJspiCUPoGXopcsuqq4f41C6QfnnVigOfaoboU/aPFxIBG0aLuScW8NkAMHBp6Er8N9KjgxX63ZgaTAIJC3eZh0MAjPvtQg9XGxRcmE+L++5SQWXfmGG/rpmoR9uAj2t1N0TmAygqLhhZPgTSh0OUssAZINBFjENBqm6ukJT0NOCiy54ss/FbcJkcEb20ZkeCX2DNg4XEogqClKYTKBXr16DlOwKVNoAnBoMUgkGoCHo5ddalV5ZzcF0kaoLU4WMvWM8Gnqj3heVe3EDkwEcCgz8CbfWiowMV8MAHB4MAvfbaw16uSpTeQ5AbcHEHG+AXtSfRl3fP5XJANJNR4Y73RWolgE4NBgEDECL0NNXWhWeIGPLinkuQL39/jqvgT5epqqSXCYTwK7A7kp0BaphAGYHgxQWFhXabAYqTtQk9PK77IrJpRZ11TwfoPh+/8gMr4M+foOkYcKNqINMBhCwbftCpUaGq2UADg0GqStOUB36QgehN73Hzlcojfydg6uQ4FgsjMlyKfRbtAE9KA6VcXwpkwEkNo4Mf9TZkeFKG4DDg0FuwWSguipNQy+/x64y/SwH2Nn9fvJpr4Y+7g9TGarKHOkKdHhkuFoGYNdgkFuUtA49fZddwTEyx7D4OgfZoQtEy4V8Mh2XQ9+oWKLC+JNMUYBSI8PVMoAmg0G2b9++wRr4ksouLdA09Kb32I0SCs/M4UDbKTgCm3V4BoceoY/9fWiDMoNXMRlAlEIjw9UwAPlgEGgGenMxmQxiC/5bt/4WysgYLWWg91UNevkFljDimoPNpsqcaCFtt6/roN/sDPTvuwR6WvGbPmUygEKFRoaraQDywSCTrYEvqSJ6gy6gl5R/bLJ4wUVNaRYH3OZ+P5hDb06/DRViKJVmRjGZwCgFRoarZQDywSCQsBhhC35QVfIBzUNvInJ/XdHFH8QooJaXBi0O+AD4r+/y5dBbgN6o94SYX98Tss//wXY4SIGR4WoZwG3YDCQNBoGxxu8bamr/1xL4kuCuPM1Db+bW2vwT34pjrTnwpqqpKBJKEo4JWUdnewf0vzsGvaRoooSAcYxdgRlXnR0ZrqYB0INBxGagLDIYxBr8oJrCeN1AL7+1Fi6uLOUmYFLfL4reJ+RfWMehtwF9g9YbxdQVWFfv9MhwNQ1AagaSBoMMSklNjbMGP6i2NF130Mtvra3Ki/F6+CsyI4TCyF3CjSvbhOs7fV0OfYIOoZcUtX6IkB95wCr4kgICti1yZmS4GgZANwNJg0Fgn9I/ODg4yJYBgPQIPa3cwC+8Nh8gDvQkIT/AD8o8Mlsx6BO1Cv1vykAv6hejEnd+bRN+UGJiklMjw9U0gBaYmewoDQYhk4ECWQxAj9DLb6yFu+y8sb5fGLWvAf68kHUcejugl8tQWWYRfElVVdVOjQxX0wDoZiAoVby1cOFCfxYDKLm0TJfQm4jcZAOjrb2mvp+X0AC+FPqn/uXLobcT+mvrGnUj9oRV+CWtWbPGz9GR4WoZgHwwiHRL0GJWA9Ar9PI77Dw9HyCW+FLPm8Avhv6Hv+PQOwD9tXWDG5QatMQm/KBr16IcHhmupgHQtwTBoYVXn3322dEsBlCRuF/X0NN32WUfHOex+QAo8RXHH6PA3ykUXt0p5J1fy6F3EPpra42KJIr+/SMmAygrK3d4ZLjaBiAfDDLcHgPQK/RZsnvsCkJ+9MgSn3G/b4Re0o3LAULKjlEuhn6Yx0BvojWDhaKkC0wmMGrUqE8cGRmupgHQtwQ9hmOMht64UVhoywDgwg29Qy+/1qo04bDHwF8OJb6rMvBRGUHfceidhN6oQaLSjq9kMgBSYXNoZLgrDIAeDDI4Ozs73ZYB1NyIZ4Y+V8PQy6+1gkGXet/viyG/DHpJuST059A7D/1VSjGbRtuEv5YIDwf1sfdwkFoGYG4wCLjTgOjomHBbBlBfU+kx0NNXWmUHTtFtPkAs8V3b1wR6SQWXtwrJ2z/n0CsA/dXVpirPTbIKvyQcGf60PV2BahuAmVuCTjM1A3kK9OI9dtRddnDDjR5LfJbAl5QeOItDryD0oAjQqoFC1oUAq+BLOnjw0M/YdNcZI2+bXYFqGwB9SxAMBum3bdu2DSwGUHBiqnug36M89HLBXXe6KfGlnLcMfoRRcLUVh15Z6GnFBUyyCT8oLb3hcBB9c5DVKEBNA2hm5pagNxctWryEqR04xN+joKdvt0knF15UaTwfUFNuLPFZgl5SfjgJ/bd9zqFXGPoG/TxQuEJUWZRjEXxaa9f9MpUaFWbzbIArDEDqBYA55q9NmjR5JosBFIX+7FHQyy+6gBHYMBdPkyW+glTT/X6EeRUQpR+axaFXCXpa+VHHmQygqtrwz8RJk96jjgjTUUAzVxuA+cEgDAZQRqbseBr08ssuYCim5kp8GRE2oTfqLyH77BoOvULQX/nZnAYIV34yKunAQiYDABWXlGZjFNCJKgne7g4DMD8YxFDzv7YMoDz5qLrQ73YP9PLx1zApRzMlvrhjNqGXlBe+RUgK+IxDryL0l2WqrihlNgFyhdgJ7Ax8iGoMarIVcIUBNB0MkmW7F8BQEOex0NPTcGFAJpTY3F7ii9xnE3pRV4xKOzjTSeiHcugZoL+0/B3h7OK+wom5bwiZoXuYDQB0PuTCIuTO4lbAFQbQZDBINkwGYjAAT4VePhgzM2i6+0p8uQnM0EvKPrNacehjbEAf7QXQh/34rnB+aT8R9qAZrwj7vukt7JrUU9iJOjL3XaE0J4nZAKoNNX8PGDiwN54SvNfcVkBNA3B6MIhHQb/N+jTcgrCNbhjUeZ4Zekl5YVuExK2fceidhL4B9nkE9pmNsEuSoN850VSnlo2waysQFh6+BvNvD2BFrgUdBbjCABweDOLp0MtVlhbqmpCflPgKowOZoad1/eAMDr0D0IfQsH9LYJ/c0wR4a9DLFfbH1/YmBJ+nmoNMzgi4wgCaDAZZt27dKqZmIDJVx9Ohp8dlpf41SvV8QGVBinAjcq9d0IPyibJI6M+htw19yNK3heAFbwpHv3tNODCtjxF2SQ5C36geohJP/MlsAph8N3tGQG0DcGowSMGZJR4NfbKZcVnph/zUu5jj+iW7oRd1+S8hN3SLkLB5JId+lTnY3xJhP0hg303DriD08PsOTO0jHJv9mnCamAtEFAXx55kMYJ2xOcjsUWFXGIDDg0GKI7fqEPoP7IZePjUH6vBKgl9NRkwXxR61G3paqQdmeD30F0lG/syivgj7yyLskpSFvocI+5FZrwqn5r8hXCCwh/7wbhPFbPdjMoDNW7YskR0VbugOdJUBODQYpJTM1PMW6OWTcyqyo5VZ9VMviUm7pO1jhJzz6+2CXlLW6dVeB70IOym/HZ/zuhA4/RUCeS+U8tAfmPoygf01Avubwnn/fkLYineFMDPAi1ou6R2xRMhiACEXLuzBeRyPU5ODXWYAZgeDkDFGBlsGUJkV7lXQ00M04GhtDbkr3hn4AWp5nf46qd9DJt8W9PmXd4iC0B8urLQJ/a/6hb4B9rkE9hk07MpDf2CaGdglMULfoO/ZDODsufP7LI0Mc6UBtMWmhB5EQ1gGg1Tnx3oV9PKz9BlH5jl2kIcYR1rQXIt1+oQtI4XMUz9ahJ5W6v7pHgV96I/9hXMEvJMEQBH2Kb3MAK8M9Pu/7SMcnvmqmP2HZp6wFf1NgXcQelosBnD6zNkDkHvD8zgmo8PVNgAfqhnoXtyDwF5kIMtgkNqKAq+DXn6lFYTo9mb5k/8az1SnT941Sci5sMEs+PnhO4Qsclc9czeeBqEPI7CfJ0k6Cfa9pNYuAq8C9BLsJwns55b0Ff9uI/DKQw+6CFrGZgDkEtGDcBLX3LAQVxiA2cEgwcGWB4PcpOSN0MuP1pZnRTHBXxR/0u7mnLgNHwhphxc2QJ+Hyr20WYjb+Kl2obcA+ymSkQ+c8aop7ApDv/fr3mJeQII9nPzdIFdBf3HZ26KurBvJaACnwQDeoq4Sd7kB0INBxGagQ4cC/7IFPygrcLJXQk+fsEvZOd5qPgB+TqzRO9Gck7DVV8g6+0uDAaTsm87Ud+8O6C+T5poLBAaA/QjJyO+HjLwcdoWgByOB6AGSgQB76A/vNADvDuhp5cedYzKA+QsW+KMBuC0CkA8GIbcELfK3Br6k3FOLvBJ6+Sm7jBPLzIf8+SlCyt5vFWjOMcIO4GecWKEZ6KGT7sLyRtghibaHrMC7v+6tOPTQjgs9+JAMhDwBwErD3gD9CvWgv2gD+gskyonbPV8oTI1gbgR66qmnx7lzCyBvBoJExOuTJk2aZQt+UB6Zoeet0MsP3NyIOmgCfwkp8TnXnMN+ws5V0ENG/tRCU9gl7Z6iHPR7yO855PeyePAGEnShBN7wlf3NAu8s9JecgD46YJqQcnydkHP1qFCSnWjXaUBQTm5eEeHtI7w/sDtWAVyaBJQPBnkSSxIf3LQBP6g4ardXQy/f08OKD/BD8k7v0Evlt2MkvD5E9tQ07EpCv+drAvv0RtgBwssrBxiB1xD0kRvGC4mHlguZl/Y4BLs5/bVz137ouyF62Vw7sCsNQN4M9D6LARQRA/B26Gkl7fhSDPn1Bv1FAoexseYNi7ArAX0D7FB6W9IIuyT1oH/HLugj/5xAYP9BhN2ecN4elVdU/qfrk09+DfdxYPm9yd2BrjIAejDIY9JgkMys7AxbBlCZF+v10OttpRdr7VL5bfqrYtbcKvBOQB9IYD82h/THL3qLJAbfNp6tXzlAGeh/UAb6BthDAfarqsBufkDout2Es88h6Y4nAjvJB4W60gDulN0SNCiLDAZhMQAOvXahD6NgP0w63PZ+3ccm8I5CD6U3yMafoWGXpBHoI34hsxL2zBfSz24RigjsVXac3VdSFy5eiiWMTcTw/1UzTUAuOQxk6ZYgGAwyIDQs7AzLNoBDrw3ow1Y2NtaIsH/TB4FXHno4bGOEva+4ipobl+Vu6CPWm8Je7SbY5UpITMonfE0jGgUDeHAS16PUOQCXHQc21wzUEcORd0iHUiC7AXDoHYN+iEPQX8by22kCIMC+nxxYEYFXAXqAHU7YwbFaOF5rbUaeu6AP/3mYJmGX6/CRI9cIW98RfUE0DBPu3bEBqI2rJwJZGgwCI4v7rl27bpVNA7h5S5yZpzfo42xAH6sh6C+To64i7CRJd/g7GewKQ3+QlN6OzqZhtz0Y09XQh//8vnjUNv3cFvHMfUVhtiZhp5VfUHDziy++3IHwT4AqGzb/PI8t+E1Wf1caAN0L8JA0GGQRmQxiDXxJWccXcOgVgh5q7RfIw94A+zQzsCsE/X5ypv0wOdMeTOr6Icvetmsarqugv7zqfSGWwJ6hI9hNZ/5dzpkxY+YhwtNiohlE44k+hGv4MPR/XDYP8DZ3GQA9GKQbNCa8N3ToJGvgSyoI28ShdwB6gB0y8gD7UbKfPkiSaHvJoRVRCkMvwQ75AYAdYLV3BLYroAfYr5/4RbhBYK8ksNfpCPbU62nVJ08Fp5Hs/qXRY8bsJQz9gODPJoJy3xhM+vVF+LvignuPpctB3GEA0i1B0Jgwwhb8oMLIXRx6G9BLsJ8hte9jc2WwKww9RA2QF6Bhd3TuvZrQS7DnRR4Vykhjja3rtTUJ+9p1l3xHj4Zmnp+IVhAtI4J5/3NxxZ9CBK2+H0NlDTv+XsB+m4dk48Cbu9MA6MEgj+NgkGGlZDCIJfAllSYFc+hl0Btr7f1E2A/NMAO7QtDvI39GEDnmCr34UAEIJ9A6e9mFGtCzwK5V8HPz8m+RiliuBdhhnNd8ojkI/LdEkzDJ9zmG+4Nxv98TT/w9ipG2tPK75W5AW7cEiYNB4JYgWwZQkRPt1dCHrjTCfoKsuEEkzN5Hwm2Q0tDLYYcav1I33CgJfdSmr4TkoBVCdtheJti1BL8E+9atAZEAe8eOHX+xAvtUXOEhqTcWgf8Yw/zB2ODzGoL/LK76HbHjto0t+F1pAOYGg8AeZWByckqsLQMwlOV5DfRhK42NNScWmMKuBvRNYBen5gzSFPRRmwnshwns4XuF4utX7YbdneCLsIeG5W4xwn6AwL7eTtg/gW0ydM1C3wwm9t7A7fNLmOHvjt21HXF7fS9utVtYCvvdZQBmB4OcOhUcZMsAQJ4IvVh+Iw0lwaSzzRzsSkIfJI2mWtJPuERWUdNRWdqAPmrzRAL7j0bY0yKFOrjBCOQE9K6Cn2xl/xsdE1tMYL82bZrfUQL7r+T5/pFoORGcx1+IsM9kgH0gru5vYB2/J07Seg4raF0xiu6E+/z2CH5ratWXsv3NrEHpagMwMxjk0F8sBpC87XNdQ395lbHWHgxjpWe/bhF2JaCXRlOdJWfaL61418J8PPdCH/n7KCFh30Ih4/xWEXZDZVkj8LQ0CL4c9h49emySwS4l6WZhRx5k6L/CZN0oO2F/Elf4LsjNQ7jSt8PF9G6s799Jgd/cFviKGgCjOVgYDLLQn8UAYECmXqA3gZ2U36CxZr8N4B2FHg7bwAk7cYAFwG51KKZ7oAfYE/cT2ENswK5B8O2AHRpw/Ii+wR58SNKNJvoUm3KG2gl7Rwr2+3CFb4Or/F240kvQ306D7yirahuA2cEgcEsQkwEcnscG/QbXQg/AXSIPOay2Yq3d7xUEXnnoYdbdcXKm/czifuQs/buMk3BdB33g0g+FK2uGC3F/TRcy7YFdQ/AD7PsPHIxf4u9/ZtDgwTvshH0kZuWHYZLuXczOv4pVrxdx3/60g7C3kAFPr/Z2N/e4wwDMDwZhMAC40srd0F9da6y1A+zHsLGmEXZloW+AnezZ4Sy9NERDC9CfXj5U2Ov/qbBhwRfCitnfCAtmzhC+nrZIVFl5pf3Auwl8AnvJ/gMHEpYsIbAPEmFfqQDsr+FdfC9hnusZbHx7XGHYmzmb2XeXATQdDMJiAPQlFy6A/hpda8eJNdAAI0ph6CFqgLwAbBlE2GWTc9wF/YUVg4WgpR8JWxeNEVbPnSz4fzetAXRLik9MdTn4dXY01hhhH/SXrNa+GDPyAPt0J2Hvjs/2I5ikexhr8vfhcXhp364I7HozAHODQYZmZmZl2OwFIFdlqQU9NNaEEyjE8hvU2kkS7YAEu8LQQ9QAWwU4ZQfZeADU3Lgsd0C/c8nnwvr5E4SlBHQ/v3k2YTenoKOn3b7q2+iis9RYM56C/SMnYW9vBvZWasCuRwOQDwYZzNQMJBoAw7FaG9BDY81lGvZZxuGTkpSEvgF2mENHEnQRqwdanZHnrpU+fucMIe3Ur8LMOcsdgp7W73/+5dJV307YrTXWDMGz830R9j4Owt4aYW/pCtj1agAmzUCXLoWesWUAtdXlDkEPGfkQzMiLsJNw+4Dfy4pDL/bHk9N1ADtUAOA8PctgTFdDH7+LwB78q5AfdVwoy002gXL1us1OGwCYiFrw55HGmjDsohvtGOzWGmt6YA/9sxTsjyoAe3M1YdezAXTGEsgAFgMA2YKehv0I2VMbYX9FcejhzzoyW4L9XTGioCfnRKoJ/c/s0MdsnSikHP1RyLm8TyhOj7QJJoTvzhoAKL+gyGnwCex/k+cib8uWrVG+vr4Hqcaa7xH2BSo01nTGWrtuYNd7BPBv8vrAYKj5XxYDoKfhWoddWegBdphoCwm6K6sGmo7K0gj0sQT2VDtgN6er1+IUMQD4c+yBPycn95+QkAuFf/75Z/zIkSOPP/zww1vIswE98qvwyKs/Aj8bk3RqNdbQGXldwK7nJKCYAyC90rtY4IctQMiPQ4VjpMPNPOzKQA+ww8UUId8bT76ZnY/nZuijNviKsOcS2EschN2cYOVWwgBMEoE2Vvrz50OK//jjj6R58+aFf/rpyOMdOnSARpvV1Fn3uQj9FEzU+SLww6kk3ZsK1tp1Bbuey4BQF+1dU1P7D4sBpJGJLUpDL4ddPGpraSimm6CP2jBaSD64SMi6ECDCXlNpvCOwTiUpkQiEXIIze/3y8or/xscn3Nizd28ImRq1tWvXrlNxpf8QV/l3cYXvg8A/ZyZJZw52R8pvuntp1QCayzsBT5w4uZx19T+5eJBT0IsDLMgJOxPYJTkM/SBFobcEO606laVYIlDh0l5efsGNy1cijs+cOWsirvY9EPxuVLLuQepgDB3KeyzsejEAev8vnQZ8vrCwKIHFALIijtoFvRH2t8RSH5ylNzsjz83QR67/QEjYPdMq7K6GX9FEYH6hat18VdWGfxKTkvetWbP2Q0zgdaFOxd1DnYprQR2Q8Vjg9WQA0kQgcSAIC/ygk8tGWIQeSm8npTPtpKZtbSimu6AH2BMJ7NkXA4SipAtCVXGOTdhdDb7iicDIWJf071dWVZfGxSf88Nnnnz+LJtAOV/9W1Jl4sz3z3ABcawD0UNAn/f39RzPt/UODGoAPJB16x/GYK8BuMjlHI9A7C7s74Vc0EXjktEtP7hlqav8mu4SgVavX9MFnrK2Z8/HNuQG4xwDk9wI8/csv66eyGEDk1mlCGNmzRxJgm4zL0gD0AHvG6d+EgujjTsPuTvBVSQS6aUgHGMHqNaIR0BNy7pRNyOFbABcbgMnNQC+99BLTIaC8sB2agT5xzywh4wzAfkIoJ110SsHuCvDJufb/p6VEoNoTeiAiSEvPWD9u3BdPUTPyWlGz8T02GtCqAcjvBuzP0gBUmZ/iFujjt002wh5DYM9TB3a14Cez6P65cOFi4R8b/kycOHHiJXJHfKZWEoGunssHOYJLoWFfUfmB1maiAW4AKhqAuRZg8XLQ7OycNGvw16Pit45VFfr47ZOFtOM/CXkRB4TS9GsugV0p8El5DAZP5m3esiWaJMKOYBfdBqKN8+bNDycr//+198+EI71KGEBoeKxQWl7bRBVVtUJldZ0oQ22dS4ygsKg4ZNQo32dxW3APRgPMs/O4ASgTAdADQfsfOHBwlzXwJeWGblcMehPYM641/j0uht4R+MtIg0xoWHgeOQxzzdd3NPTH/0Y+x5/xUIykVWR7FUCGXZQ6aiow1MP5LcAK4UBQiJBbYGBSQZFBKCypEQ1CLWOAbcHFi5cmYjTQ1p7pudwAlMkBtMEcADRw9Bs/fvxcW/CDaqrKheg/PrYb+phNY4SUwMVNYaelUfAB9pjYuOKtAWQWnV/DLLqV2CIrnX5biD3y8/F/F/322+/nyisq/uvsNmLBklVOGcCipeuFjVsPMRuAJVMoLqsRDUFJI8jKztmBC1F7TEx71JZA61UAaSAotHJ+UlJSarAEPq3ilItWoY8lsKcGLhFyLm0TYQfTsPVnagV+C7DLZ9HNoybWTMWpNVNQXz/22GNzkpKT85TKI8C5fkfh/27ej8KyFRtEOWMAtPJuGISiUuXMoKS0LHrkyM+ew5Ih0yUa3ACU6QOg7wZ8f/fu3fvrGQwAVJoZJaQGLRGS9n6HsG8nsEexwa4h8AH2AwcPxVuBXT6LDibWfOljvPwReuI/w8k1oM9nzpq1sqKy6j9KgF9ZVSeG4ocOhwjfTvd3KPSX4AfFJOQoZgKS8gsNQllFrdPbBGK8GR9+9NG/sIX4XjN5AW4AKnQCtqOmAQ18slu3ySRT+x+7AHZGLoY+lsB+kMDu77/0zGDHpszCeKr38RDMIBxk0R+Pvb53KDBou7PQ19TWi3tvAEuC7GpUuuC//HdxNWcB/xu/xcKcBatM4AeduxiruAHQUQG8b2eMoNpQ8/fmzVvew/6Utp5gAlo1ALoXoANOXoFZa58GBR0+5QngE9hLSGIzgXQ5SrA7MmX2feqYK4yneh2jpd543LU3/v83ExKTzisBPoAkhys9q6wBYjACgHvG7OXCtJlLG6CH/4Yfm7dotfhr5PCD7EkEOmsEzpjAnxs3DcXnkjYBXW4HtH4vgNQO3BWPcw6D456qRgEqwJ6Wll4dHByctm7dL5cUnjIrzaKTxlM9hUddu+N/P//6G2/0JXMUr6gBPq0163eYhdoeOZsItHdr4GiOAExg/oIFb3mCCehhIEhbPMEFD/k7sI8lFzFs0Sr4NOyjXTNlVhpP1REfyI74eXV9993+L5eWlWU7s8enQ31r2rbzmNMGoGQikFWQw3BkW0B6JjKHDRv2Em4H7sVnVXfVAS0bgLQNuBsTL3CW+xUMeyeQ6a7h7gbfTtjVmjLbDk2yLZ6ehM+qy5D33utJEldZjoBvqKkXbhTX2AXSkRNhihiAGolAlmigymCHCYBhEBUVFcdidPogVgekEiE3ACcNgK4GSMnALghEPx/jHWrfkEaNOFfBn0+66MLCwnMDAraJU2YduKtdiSmz9CWP0ngqSXfjz3cYPnzEiwT+TIcaeypsh/vmBIlAJQxAzUSgLZVX1jKBTys19fpuH+MosQfwO2ihp6Sg1g1AHgV0xeTWIAyZ/Y4dP35VafAVhl3pKbP0xJo78P+3wl8Ln9FjBTcKLzqy14dw2FF46ESgM3JFItCaoH+AFf4a1NFjx6ZhdHYfmrFu8gFaNgB5FNAW97fQGARjnoYicNPHT5gQcKOwqN4R+GGmHIE9L4A01hDYD1gZKa0E7EpMmaV1OxrA3fjnPJKTm3fUXvirDfXMe31r+m3DXl0lAplMwAz4NPwgMnXo7wEDB/bGiE1KCkr5AG4AThpAc6oicB/C8xyWvIZhwwuAuWDWd98duHIlIruiovK/5sAH2KHWDrD7mW+sWehjelc7DbszI6WVnDLbjEqS0p9L5+iYmB8dSfQ5EvKb0+59wbpMBFo0ARvg0yLGG4rf+UNUPkDzWwGtGwBdEWhBrXQQMj+PCbMhuBJDNn0mrtjLevbq9cfYseP2jBkzdt+YsWP39uzZ808LsJurtftinkFN2B0dPCmZojQ1WYyM9u0/MNpe+Msr6xSF5tSZq4oYAOQTNGECJTVM8EsKDAqajs9Be/y+Nb8V0IMB0FuBOxGm+3HP9SxmzKFc9gGCOxEjgpkYus9FzcYfs3V98yAsN76JsEvz490BuzVDlE5MPjRs2Psvwek1d8KvZCIQjEQLBgAqK6+xCb4kkngtx2dS2gq01HpVQE8G0Fy2522PibPuCOjrWEp7H0N1Xwzdx6Gk3niW65vpyyJcdlc7I/xSYrQ1JgwfJ2OtLrkbfklKGABsJbRiACCYScBqAlFR0ZvxuXmQqgpoNgrQiwGYM4HWmDx7GFfkpzEsfxlX73ew3DYQ1R/DeEuNNd18ml4W8YAbYbcV+oul0WtR0SvtuV4bSl1qwqJEIhD+DC0ZQB5RdQ2bCZAu1X/69ev3Gi4a7aiEIDcAJw2AhkDKCbRCMNujETyCZbWncRX/N0YHL2Kd/Tn8uW4+Gryr3c7Qv8PgwUN6MYX+OGKrsqpWdVg8KRFo0jFYbGCOAi5cvLgOI1MpIajZKEBvBmApGrgLP+h2GKI/jCF7Z3TiLlS7rGbvarcz9H8iMyv7OCv81Qblsv3elAiUNwqx5QLKy3HxeUTrUYBeDUAeDdyOcLSkuuLuwdCdVhvZyq6XG13l/RCdd+7aPY4FfBA8lDAxxxWQeGIisKFl+AZ7FLB7z545VBSg2VyAng2AhkNuBnfgB36nTLq7vtlMRyQ8UN3I4Mo4FvhBBXlFLgXFExOBDVWBCraqQEZm1hXcdnahKgK3cQNQ3gDkRtCMgrq5GdD1dudbM1ni75Ht23d8yQK+q/b93pAIdCQKeOWVV97BisADVF8ANwCVDMCWMejxRa/+bXD1f6qwqCieBX54CF2x7/eWRKC9UUBg0OEfMfHcEbekd2ptG+ANBqDnF736ixelBmzbPt4W+JKKS2vcAognJwLtqQiQ24YifIwnPR/F709z2wBuADpb/clDdYoFfsj6uwsQONPvqYlASVWGWpaegP/xMR5c66bVbQA3AO2v/g3DUfv27fu6LfAl2TvQgycC7VMpY4vw7NlzxmN7cAdZTwA3AG4AVl/0/QjiRKRLl0LXscBfVV3ndkDgWK+zBgBzBrVqAKzbAHJIaxU2oknVAE2dEuQGoN3VX+r6a4tNTP8iF6PksBiAu/b+tGCwhxJRAAwa0aIBQHswiwFERFw96mNsO38Cm8801RTEDUDb4f9d+NA8MWHChGEs8Btq6jQBCIz28uREIKiy2nYegFwtluJjPHvSHSM5TeUBuAFoN/yXGn+gdfnpkJAL61kMAGb6aQEOpRKBWjYAltZgcgsTJAL7ajUPwA1AH+H/C5mks4zFAJQY7aWlRKCWDaCkjC0ROGPGzEnYFQjf5b1UHoAbADcAq7V/CP9hHkHv6mrDP3oJ/5VMBGrZANIyi5gM4NjxExupfoB2WuoH4AagTQO4A/eKsGfsvnDhwrF6Cv+VTARqFX5QXGIOkwHExsWH+BjnVMBR9fsxt3M7NwBuANb2/9A6Ci2kz23btn2hNfClCbbOjPVWQ6GXkzy2D0A6+ZiZnW/TAMix7VQf48QqzSUCuQFoe/8PteMXQ0NDd1oDX5I7+v5tyZk7A5NSCzVvABGR8UxRgI/xIhg6EXiHFhKB3AC0aQCwR7wP9/+90tMzrtqCH+630yokershyJ5/25lzl1kNAGZPwvi5ThjdteAGwA3AWv0f9opwlPSVnJzcFEvgS6qsrtMsKPb2BOgBfskAdu09zmQA0/z8pmixI5AbgMYTgLB3LCsjc3xtXFip9rBPJfIBtrYDsOfXetgvP/UYsCOQyQC+X74cJgTBfRKPaakSwA1AewlAqf8fTv/BANO3mK6rLq/VzaoJNwnT0nKpz9aNyKwGsHTpsnk+TVuCuQFwAzBrAG0wWQRJo36eZACepG07jzEbwBJ/f7ix6hWtlQK5AWi7BAijzd/hBqBNwdgyVgNYvHgJXEX3qk/jiDBuANwAzBqANPcfssXQPtqfG4A2BXkLVgNYtGjxIp/GQ0GSAdzBDYAbgDkDgH7xzmgAA7gBaLe8yWoAC4kDaLEZiBuANpuAJAOAyyUGcgPQnqQ254NBp5kM4KuvJs6kDOABbgDcAFgiADCAAXnk9s9anZcBPU1SSdOORqCPcAvQjecAuAHYlQMgl0yk2TIALTcCeZroWQex8SmsBvABVgGe5FUAbgAsVQAwAGgdfTcpOTnGlgFotRXYk8N/EMthoOtpaRnkexxO1MdHY6PBuAFouw8ALpV4+9Sp4ECWPICWhoF4sn5ctUWEf+XqLUyr/5WICLgmbChRLx/j+Q7N3BHADUC7nYAwCuwZ6ARcs2btKhYDKCqt4YC68FwD6zmAXbv37CXf42AfDQ4F4QagvUpAk7MAg4cMmcJiADwR6NrjzaxHgceMGQtNQAMwqUuPBeOnAbkBNDGAJqcBIYFUVFxisGUAsB/lkLruVCM5o2UT/vKKyv+Q728UbOWws7Ojj4YGg3ID0GYvgHQXoDgPkGgYmS9/hSUK0OvBGq0L7ieQ9v72hP/RMbFJ5Pv7hOhNH+Phrodwi8cnAnEDsGgAsD9sS/QI0UtEg44dP36ExQCOnQrnwKp08o9e/VnLf7/++tsO8v2NoEqAmukB4Aago1LgnLlzl7MYwMGgM5q9TccT6v6gdb/9xQQ/qGvXrt+Q72+IT+MsAE3dEswNQCeVgEGDBn3DtAW4Fi+uVhxcZU/90QbAmvyLio5JJt+dr0/jODD5vQDcALgBWEwEtsZwEVpHoYX0Q5ZE4I3CEnGvyqMAdUab27P6kxkAcB/Ax0RvmNn/85uBuAHYTAS2x84xMRF4hTERuGHTPvHB5QArP8uQdfUvuFFYS76zCdgARE8C0sz+nxuAfhKBL0Ii8M+NGzezbgPgYYW9KwfZ8X0/nfUHbdi0l3n133/g4Gkq/IczHfx6cG4ADiUCpclAb3fv3n0CU0NQRZXYpgp7Vw6z8yU/e/r+QWXlFf95/PHHZ8K2zcd4BPgpKvzXzMWg3AD0kQh8CB8geJA+jo2LS2StBsBDy7cC9sMvT/rZc+wXtG///rPkuxrn09j++5gWw39uAPrpCIRBknCSbNjvf/yxjcUAIBkoPbwwkpvD7Tj89oT+ZPX/P4899vh32Pzzlo9xsGtHjOY0Ff5zA9BfHmDgk08+ORnaS1lM4Mz5y+IDDOEszwc4Bj9spQpuFDMbwKbNm4+R7+kLrP33wuSfdP5fM9l/bgD6yQPQI8JhRRkZFn75mj25AG4CthN+li4tYe34A6VnZJaR7+cbXP37+hiPc3fC2n9Lra3+3AD01Q8AbaRwxfT7ffv2m8diAKDY+NSGhxkecm4CTYd7mkv42VPykzRp8uQNuPeXr/6ttbj6cwPQzzagHW4DxBmBRKNDQ8OircJPHkhJMLhSeqh5JGB6tZela8pYh31KOnrsWAT5XuD+P5j99yZGbJpe/bkBaN8A6G0AtAVDNxl0lX305ltvLWSBH1ROjq1CIos2AW8+NQj7/Y1bDykGf1p6Rvmjjz46H4wZ8jSY+X9cy3t/bgD6qwa0x4eqJ5aXxp08dSrMGviS4CGFGraUD5AEK6C3wQ8VEUshvyPwl5aV/58RI0asJ9/HVz7GuX+voVF30GrmnxuA/rYBd1JNQVIy8GPSbDKroSJgAXxaYALyBx7ut/OGcwNw6zD8W63dTmxPrV/Sih9XBmHi71Mf49CPF3C7dp/WV39uAPpqCpJ6Ap6gooCxCxYu3MYCvyRIbMkffFgRPbVXAMwNTkdaW/UdSfiBzp47n0C+gxlEY/D76IU9Gw/6NHb9aXb15wagvyjgXowCnsFcALSaTo6MjLxuC3xbJgCCfTGslJ50mMdSeY+u87O2+NKKi08oIJ/9bKLxUJmhQv+OVOLvdi3Dzw1An1EA5AIe8zFOCoKKwKhHH31sbjnpQLPnATaXE5C0e1+wbo0AVnwW8KV7/Vjm+jVN+qVXdOnSZSn57Cdh1h+2ZP+yEPpzA+AGoGgUIFUEYGIwjJkaRvTlBx98uNbeBxlMgK4O6NkI4H3CuQdbob4z+33jJR/plQT+78ln/jXu+9/xMXZpPo79GroI/bkB6DMKgJCyFfYFwPHS53H1gVVo8sqffjpo7wMNKyDdJ2BpawCrqlZXe2slPXOrviMhvwR/586dfyCf9bdEn2ME1gubtB6isv636wF+bgD67QuQugMfx61Af6LP4ME8HxIS78jDDS2vlrYEdLIQogJIGLqrcgArPZQvbWX0ze31HUn0yeBfQT7jaVjvh6RfH4zEOsj2/c25AXADcEVZELYC3fBBHIzZ6Onnzp9PcOQhZ4kG5JEBZNihqUgtQ4CuRVjlwXhY9vXmwIdw35G9vhn4/fAzfg+3X5D064QRWSu97Pu5Aeg/CpC2Am3xAXwGs9CQD4CTaLNIiSrR0Qc+JTVTDJXthQ0AlUxBMgZJlgyC/jWwssPvg9Xd3Mk8V4MPIgevsqiVH+Afip/1s7gNo5N+t+kJfm4A+jYBqSpwH5UPgNIgzKCHWXSzz549l+jMw++oEbhTMLRTCfBBhwKDosnnCNd6TcWw/z2E/zn8zNvjdqyFHuHnBqD/rUALzDrfj6VB6ELri/0B0Jo6O+jw4WvOggBJM3u2Bu4Q3NRjz9FdG+29/50xY+Yh8vlBfz90+cHVXnDC71Vc+R/Bz/xuPcPPDcCzSoPQffYElqTexsqAaALLl/9wVAkwYFWFRBrAphXo4f0osdo37Pevp1X26tXrV/K5zcE6/0gf4wGfl3GrJa38d/tovM+fG4D35ANaYlIQSlFdsTLwNkYCsB2YNXTosI1wcEUpUCQzgMgAwm5XAA89C8dOXFBspZdr27btV8hntYRopo+xww9M9F0s9T2F+Zb7MOy/U28Zf24Anm8C91Im8CJuB0ZgYnA6JLPCSVJLDXhgbBaACftvWJmtNRix7OMh9wCwXwy7JuYi1HjPklKvp1UNGTJkK/mMFuB+f6yP8WRfXzTTJ7HU187Mnr+Znh8gbgCelRRsRZnAE5gTeAOrA5DBhgaW+eTCynOwz1UTKnkykUVKhvJse/2y/677Zf0F8plAWy/09U/2MTb4wH4fpjD/Cz/Hh7Dicpfe9/zcADzfBKTtwIOYGHweM9fQJ/AZPuSzO3Xq/BMpcWW7Ejgt6cDBg3GdOnVajas+lPi+xJC/P/ZVSMm+B/DzbKnXUh83AO/cDrTBTHUXTF71wYf7I3zYoall4dix43ZBCOwt4J86FXy9R8+eMLtvMeRGMNEHWX6o77+FIX833O/TyT7d7/e5AXiXCdyJD+99+DB3w4f7LdwSjMJoAGbYL1m6bNnJ3Lz8mx4Nfg8RfH8M97/Bvf4HaIwvY7QE7dUPy0J+j4SfG4Bnm4DUJ3AXPswP48MNDzm0sQ7AKsE4hAHKXv5gBNExsUWeAD0xtFtbAwKuduzYcS2CPwfzIJAU/QS3RW9gwhR6+jtj1HSPT2Nrr0ck+7gBeJ8JSH0CUnLwHtzPdsGHHaKBNxGCTxCKbyUjGDxkSMCp4NOpJaVl/9Ub+CfJau/nN/0w+Xf8gKG+tOJL4A/BSKgnbo8ew0RfO08q8XED4C/5lqA1PuQP40MPia5eWO4aQhnBNwjNYkiU+S9dGhwaFpajVeDBpC6FhuUu8fc/3bFjp7WY1YcuPhjXNQVD/Y/x39gX/83PYYa/I+7126BRSll+j4efG4B3bgla4cPeHh/+JxCG3pQRfIzQTEGIAKalHTt1WgMrK+ynIbx2J/SpqderyBXc8aNHj95H3tuPCP0CzGlAJDMB8xywxx+E0Q4NficM9+/FbZJ81W/mDQ8HNwDv2hLQ0cBd+PDfjzB0RTh6ISyDEB6AaDxGBTPRDKBbbnmPHj3+JKtuMIBI8gbFam0XUlKvV8MKv2VrQKTv6NH7yd+9Ev5+fB/zMZsPDTzQ+jwaDQyy+u9gCfQlDPXl4Evh/h3etOpzA+DRgJQbkLYFtBE8gVuDHgjPOwgTlA990QwgMvDDbYJkCN8TrSAJt19gVZ42bdpRAHbLlq3XAN7o6JjiqOiYEgsqjo6JKd5Mfu2WrVsj165dd8nXd/T+QYMHb0fYYS+/DPfz83GV98P3MR7f18dY3eiPBgYRzb8w3wHbnQ4y8Ft6M/jcALgR0EbQUmYEHRCa7ghRb8yWQ1/8exgZQFPRGAy1p+AKPANNYZ6P8RjtYsy+L8MVG0BeIdMP+HPfYxgPZrIIQZ+Lq/t0DOsnI/Dw947E9/Eevi94f9DrANenPY1G1hmTe/dhEvQub1/xuQHwl62I4C6E5T6EpzPC9BSaAWTOX8V8wQAEcAQmEEchnF9iOA7Afo3wTkOQZ8g0HVfzqbjNADOZiKCPw5D+M1zhh2OOoj/+/a/i+3kBoe+KVY6H0cja+hh7IVpx8LkB8Jd9RtAK4WmLCUPJDKCXoBtuE15AAF/BFfhthHMwbhuG4yoN8H6KqzbA/Dmlz/DnwEA+RDMZhqAPxNUdYIfe/Jdxa/IC/v3d8P1IK70EfRs0spY+jY08Hl3P5wbAX0omC29DaOio4G7cIkBk8ABuE7rgVuFJjBCeQzhfwmRiH1ylX8d9+VsIcz9UX/yxN9FAXkMz6Y2gv+hjbFx6FrcjsMI/isB3wPdxH76vuy1A35yDzw2AvxwzguZmzKAV5gvaUIZwP67AHRDOR9AYnkBz6I4GAWH6Mwi0pGfwx5/CFb0rruqPosF0wpD+Qfx72uHf2wbfBx3ec+i5AfCXymYgGUILBK8lFSFIptAWQW2P0D6ABvEQwtwB9TDqIQT8Afz191Gg34N/dmtqhb9Ttspz6LkB8JcLzcCcIdxBmYJkDK0Q2taou61IAlyCnAb9DtkKLweeQ88NgL/cbAiSKciN4XYKYFu6XQb5bdSf2YwDzw2Av/RpDHKDMKdmHHLPMID/D/r+VOGJMlyYAAAAAElFTkSuQmCC')

PRESENTER_FRAME   = ((100., 100.), (1024., 768.))
MINIATURE_WIDTH, MINIATURE_MARGIN = 120, 5
MIN_POSTER_HEIGHT = 20.

CR, ESC, DEL = (chr(k) for k in [13, 27, 127])

HELP = [
	(        "?", "show/hide this help"),
	(    "h/q/r", "hide/quit/relaunch"),
	(   "f/F5/⎋", "toggle/enter/leave fullscreen"),
	("./b/w/m/s", "toggle black/board/web/movie/slide view"),
	(      "v/c", "show/hide video view/color picker"),
	(    "←|↑|⇞", "previous page"),
	(    "→|↓|⇟", "next page"),
	(     "⌘←/→", "back/forward"),
	(     "⌘↑/↓", "previous/next frame"),
	(     "⌘⇞/⇟", "previous/next section"),
	(      "↖/↘", "first/last page"),
	(    "space", "toggle page transitions (if any)"),
	(         "", "play/pause movie (if in movie view)"),
	(         "", "start or stop timer (other cases)"),
	(        "t", "start or stop timer"),
	(        "z", "set origin for timer"),
	(      "[/]", "sub/add  1 minute to planned time"),
	(      "{/}", "sub/add 10 minutes"),
	(      "</>", "step movie/animation backward/forward"),
	(    "+/-/0", "zoom in/out/reset speaker notes or web view"),
	(        "l", "toggle pointer/laser/spotlight"),
	(      "p/P", "reduce/augment pointer/laser/spotlight size"),
	(        "e", "erase on-screen annotations"),
	(        "x", "switch screens"),
]

def nop(): pass


# handling args #############################################################

name, args = sys.argv[0], sys.argv[1:]

# ignore "-psn" arg if we have been launched by the finder
launched_from_finder = 'presentation' in os.environ.get('XPC_SERVICE_NAME', '')
if launched_from_finder and args and args[0].startswith("-psn"):
	args = args[1:]


def exit_usage(message=None, code=0):
	usage = textwrap.dedent("""\
	Usage: %s [-hvip:d:] <doc.pdf>
		-h --help          print this help message then exit
		-v --version       print version then exit
		-i --icon          print icon then exit
		-p --page <p>      start on page int(p)
		-d --duration <t>  duration of the talk in minutes
		-y --youtube       do not use invidious instance
		<doc.pdf>          file to present
	""" % name)
	if message:
		sys.stderr.write("%s\n" % message)
	sys.stderr.write(usage)
	sys.exit(code)

def exit_popup(message):
	message = textwrap.dedent(message)
	command = """
	tell application "System Events"
		display dialog "%(msg)s" with icon 2 buttons {"Ok"} default button 1
	end tell
	""" % { "msg": message }
	os.execv("/usr/bin/osascript", ["/usr/bin/osascript", "-e", command])

def exit_relaunch(path, page):
	os.execv(__file__, [__file__, '--page', str(page), path])

def exit_version():
	sys.stdout.write("%s %s %s\n" % (os.path.basename(name), ID, VERSION))
	sys.exit()

def exit_icon():
	sys.stdout = sys.stdout.detach() # so that sys.stdout.write accepts bytes
	sys.stdout.write(ICON)
	sys.exit()


# options

try:
	options, args = getopt.getopt(args, "hvip:d:y", ["help", "version", "icon",
	                                                 "page=", "duration=",
	                                                 "youtube"])
except getopt.GetoptError as message:
	exit_usage(message, 1)

start_page = None
presentation_duration = 0
use_youtube = False

for opt, value in options:
	if opt in ["-h", "--help"]:
		exit_usage()
	elif opt in ["-v", "--version"]:
		exit_version()
	elif opt in ["-i", "--icon"]:
		exit_icon()
	elif opt in ['-p', '--page']:
		start_page = int(value)
	elif opt in ["-d", "--duration"]:
		presentation_duration = int(value)
	elif opt in ['-y', '--youtube']:
		use_youtube = True

if len(args) > 1:
	exit_usage("no more than one argument is expected", 1)


# application init ##########################################################

# using bundled pyobjc
python_version = '%s.%s' % (sys.version_info.major, sys.version_info.minor)
for path in [
	('..', '..', '..',),
	(),
	('..', 'Resources'),
]:
	sys.path.insert(0, os.path.join(
		os.path.dirname(os.path.realpath(__file__)), *path, 'packages', python_version))

try:
	from objc import setVerbose
except ImportError:
	exit_popup("""\
		The Python executable referenced by
		'/usr/bin/python3'
		can not import the PyObjC package.
		
		For Présentation.app to work, you have to install the PyObjC package for this version of Python.
	""")
	
setVerbose(1)

from objc import nil, NO, YES

from Foundation import (
	NSLog, NSNotificationCenter, NSUserDefaults, NSAffineTransform,
	NSObject, NSTimer, NSError, NSString, NSData, NSArray,
	NSAttributedString, NSUnicodeStringEncoding,
	NSURL, NSURLRequest, NSURLConnection,
	NSURLRequestReloadIgnoringLocalCacheData,
	NSKeyValueObservingOptionOld, NSKeyValueObservingOptionNew,
)

from UserNotifications import (
	UNUserNotificationCenter,
	UNAuthorizationOptionProvisional, UNAuthorizationOptionAlert,
	UNMutableNotificationContent, UNNotificationRequest,
)

from AppKit import (
	NSApplication, NSBundle, NSEvent,
	NSApplicationDidFinishLaunchingNotification,
	NSOpenPanel, NSFileHandlingPanelOKButton,
	NSColorPanel,
	NSAlert, NSAlertDefaultReturn, NSAlertAlternateReturn,
	NSWindow, NSView, NSSlider, NSMenu, NSMenuItem, NSCursor, NSPopUpButton,
	NSViewWidthSizable, NSViewHeightSizable, NSViewNotSizable,
	NSWindowStyleMaskMiniaturizable, NSWindowStyleMaskResizable,
	NSWindowStyleMaskTitled, NSWindowStyleMaskBorderless,
	NSWindowStyleMaskFullScreen,
	NSBackingStoreBuffered,
	NSCommandKeyMask, NSAlternateKeyMask, NSControlKeyMask, NSShiftKeyMask,
	NSGraphicsContext, NSZeroPoint,
	NSCompositingOperationClear, NSCompositingOperationSourceAtop,
	NSCompositingOperationCopy, NSCompositingOperationExclusion,
	NSCompositingOperationDarken,
	NSRectFillUsingOperation, NSFrameRectWithWidth, NSFrameRect, NSEraseRect,
	NSRect, NSZeroRect, NSUnionRect, NSContainsRect, NSPointInRect,
	NSColor, NSGradient, NSColorSpace,
	NSFont, NSFontAttributeName, NSForegroundColorAttributeName,
	NSStrokeColorAttributeName, NSStrokeWidthAttributeName,
	NSParagraphStyleAttributeName, NSMutableParagraphStyle, NSTextAlignmentRight,
	NSUpArrowFunctionKey, NSLeftArrowFunctionKey,
	NSDownArrowFunctionKey, NSRightArrowFunctionKey,
	NSHomeFunctionKey, NSEndFunctionKey,
	NSPageUpFunctionKey, NSPageDownFunctionKey,
	NSPrevFunctionKey, NSNextFunctionKey, NSF5FunctionKey,
	NSScreen, NSWorkspace, NSImage, NSBezierPath,
	NSImageNameSlideshowTemplate, NSImageNameEnterFullScreenTemplate,
	NSRoundLineCapStyle, NSRoundLineJoinStyle, NSEvenOddWindingRule,
	NSLayoutConstraint,
	NSEventTypeApplicationDefined, NSEventSubtypeTabletPoint,
	NSColorPanelModeCrayon,
)

from Quartz import (
	CGShieldingWindowLevel,
	CGPDFDocumentCreateWithURL,
	CGPDFDocumentGetNumberOfPages, CGPDFDocumentGetPage, CGPDFPageGetDictionary,
	CGPDFDictionaryApplyFunction,
	CGPDFDictionaryRef, CGPDFArrayRef, CGPDFStreamRef, CGPDFStringRef,
	CGPDFDictionaryGetObject, CGPDFArrayGetCount, CGPDFArrayGetObject,
	CGPDFObjectGetType, CGPDFObjectGetValue,
	CGPDFStreamGetDictionary, CGPDFStreamCopyData, CGPDFDataFormatRaw,
	CGPDFStringCopyTextString,
	PDFDocument, PDFAnnotation, PDFActionNamed,
	kPDFActionNamedNextPage, kPDFActionNamedPreviousPage,
	kPDFActionNamedFirstPage, kPDFActionNamedLastPage,
	kPDFActionNamedGoBack, kPDFActionNamedGoForward,
	kPDFDisplayBoxMediaBox, kPDFDisplayBoxCropBox,
)

from WebKit import (
	WKWebView, WKWebViewConfiguration,
)

from JavaScriptCore import (
	JSContext
)

from AVFoundation import (
	AVAsset, AVPlayerItem, AVPlayer, AVPlayerLayer, AVAssetImageGenerator,
	AVCaptureSession, AVCaptureDevice, AVCaptureDeviceInput, AVCaptureVideoPreviewLayer,
	AVMediaTypeVideo, AVCaptureSessionPreset320x240, AVPlayerItemStatusReadyToPlay,
	AVLayerVideoGravityResizeAspect, AVLayerVideoGravityResizeAspectFill,
	AVAuthorizationStatusAuthorized, AVAuthorizationStatusNotDetermined,
)

from CoreMedia import (
	CIImage, CIFilter, NSCIImageRep,
	CMTimeMakeWithSeconds,
)
NSEC_PER_SEC = 1000000000


_s = NSString.stringWithString_
def _e(result): # some binding version returns tuple with error
	result, error = result
	if error: raise RuntimeError(error)
	return result

def _h(s):
	h, _ = NSAttributedString.alloc().initWithHTML_documentAttributes_(
		_s(s).dataUsingEncoding_(NSUnicodeStringEncoding), None)
	return h

right_align = NSMutableParagraphStyle.alloc().init()
right_align.setAlignment_(NSTextAlignmentRight)

app = NSApplication.sharedApplication()
app.activateIgnoringOtherApps_(True)

bundle = NSBundle.mainBundle()
info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
info['CFBundleName'] = _s(NAME)
info['NSAppTransportSecurity'] = {'NSAllowsArbitraryLoads': YES}

NO_NOTIFY    = '.'.join([ID, 'no_notify'])
RECENT_FILES = '.'.join([ID, 'recent_files'])
user_defaults = NSUserDefaults.standardUserDefaults()

ICON = NSImage.alloc().initWithData_(NSData.dataWithBytes_length_(ICON, len(ICON)))
cursor = NSCursor.crosshairCursor()
CURSOR = cursor.image()
X_hot, Y_hot = cursor.hotSpot()

LASER_GRADIENT = NSGradient.alloc().initWithColors_atLocations_colorSpace_(
	[NSColor.redColor().colorWithAlphaComponent_(alpha)
		for alpha in [.5, 1., 1., .5, 0.]],
	[.1, .2, .4, .4, 1.],
	NSColorSpace.deviceRGBColorSpace(),
)

def image_from_template(template):
	image = NSImage.imageNamed_(template)
	f = CIFilter.filterWithName_withInputParameters_(
		'CIColorInvert',
		{'inputImage': CIImage.imageWithData_(image.TIFFRepresentation())},
	)
	for r in image.representations():
		image.removeRepresentation_(r)
	image.addRepresentation_(NSCIImageRep.imageRepWithCIImage_(f.outputImage()))
	return image

PLAY        = image_from_template(NSImageNameSlideshowTemplate)
FULL_SCREEN = image_from_template(NSImageNameEnterFullScreenTemplate)


# presentation ##############################################################

restarted = False # has the application been restarted before actual launch

if launched_from_finder:
	# HACK: run application to get dropped filename if any and then stop it
	class DropApplicationDelegate(NSObject):
		def application_openFile_(self, app, filename):
			if filename != os.path.abspath(__file__):
				args.append(filename)
		def applicationDidFinishLaunching_(self, notification):
			app.stop_(self)
	application_delegate = DropApplicationDelegate.alloc().init()
	app.setDelegate_(application_delegate)
	app.run()
	restarted = True


if args:
	url = NSURL.fileURLWithPath_(_s(args[0]))
else:
	class Opener(NSObject):
		def getURL(self):
			dialog = NSOpenPanel.openPanel()
			dialog.setAllowedFileTypes_(NSArray.arrayWithObjects_("pdf"))
			if dialog.runModal() == NSFileHandlingPanelOKButton:
				global url
				url, = dialog.URLs()
			else:
				exit_usage("please select a pdf file", 1)
			app.stop_(self)
	opener = Opener.alloc().init()
	opener.performSelectorOnMainThread_withObject_waitUntilDone_("getURL", None, False)
	app.run()
	restarted = True


file_name = url.lastPathComponent()
pdf = PDFDocument.alloc().initWithURL_(url)
if not pdf:
	exit_usage("'%s' does not seem to be a pdf." % url.path(), 1)


# tmp dir for embedded movies

TMP_DIR_PATH = tempfile.mkdtemp(prefix='%s-' % ID)
def cleanup_tmp():
	for p in os.listdir(TMP_DIR_PATH):
		os.remove(os.path.join(TMP_DIR_PATH, p))
	os.rmdir(TMP_DIR_PATH)


# structure #################################################################

# we'll need to look for info only available with low level CGPDF API

_pdf = CGPDFDocumentCreateWithURL(url)
_page_count = CGPDFDocumentGetNumberOfPages(_pdf)

def cgpdf_dictionary2dict(d):
	res = {}
	CGPDFDictionaryApplyFunction(d, lambda k, v, _: res.update({k: v}), None)
	return res

def cgpdf_array2list(a):
	return list(
		cgpdf_get(a, i)
		for i in range(CGPDFArrayGetCount(a))
	)

def cgpdf_stream2str(s):
	data, fmt = CGPDFStreamCopyData(s, None)
	if fmt != CGPDFDataFormatRaw:
		raise TypeError('unsupported data format: %s' % fmt)
	return data

def cgpdf_get(data, *path):
	"""walk the pdf dict/array structure"""
	try:
		head, *path = path
	except:
		formatter = {
#			CGPDFDictionaryRef: cgpdf_dictionary2dict,
#			CGPDFArrayRef:      cgpdf_array2list,
			CGPDFStreamRef:	    cgpdf_stream2str,
			CGPDFStringRef:     CGPDFStringCopyTextString,
		}.get(data.__class__, lambda d: d)
		return formatter(data)
	getter = {
		CGPDFDictionaryRef: CGPDFDictionaryGetObject,
		CGPDFArrayRef:      CGPDFArrayGetObject,
		CGPDFStreamRef:     lambda s, k, _: CGPDFDictionaryGetObject(CGPDFStreamGetDictionary(s), k, _),
	}[data.__class__]
	try:
		head = head.encode()
	except:
		pass
	ok, o = getter(data, head, None)
	if not ok:
		raise LookupError('wrong key %s in %s' % (head, data))
	ok, value = CGPDFObjectGetValue(o, CGPDFObjectGetType(o), None)
	if not ok:
		raise TypeError('unable to cast %s into %s' % (o, CGPDFObjectGetType(o)))
	return cgpdf_get(value, *path)


# durations of pages

durations = {}
for page_number in range(_page_count):
	_page = CGPDFDocumentGetPage(_pdf, page_number+1)
	_dict = CGPDFPageGetDictionary(_page)
	try:
		durations[page_number] = cgpdf_get(_dict, 'Dur')
	except LookupError:
		pass

class PageTurner(NSObject):
	def turn_(self, timer):
		next_page()
		refresher.refresh()
page_turner = PageTurner.alloc().init()

_auto_turn = True
duration_timer = None
def handle_turn(page):
	if not _auto_turn:
		return
	if page in durations:
		global duration_timer
		if duration_timer:
			duration_timer.invalidate()
		duration_timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
			durations[page],
			page_turner, 'turn:',
			nil, NO)
	if page in autoplay_animations:
		for a in autoplay_animations[page]:
			toggle_play_pause(a, False)
			advance_animation(a)

def toggle_auto_turn(auto_turn=None):
	global _auto_turn
	if auto_turn is None:
		_auto_turn = not _auto_turn
	else:
		_auto_turn = auto_turn
	handle_turn(current_page)


# navigation

recent_files = user_defaults.dictionaryForKey_(RECENT_FILES)
recent_files = {} if recent_files is None else recent_files.mutableCopy()
if start_page is None:
	if url.path() in recent_files:
		start_page = recent_files[url.path()]
	else:
		start_page = 0

page_count = pdf.pageCount()
first_page, last_page = 0, page_count-1

past_pages = []
current_page = max(first_page, min(start_page, last_page))
future_pages = []

def _goto(page):
	global current_page
	current_page = page
	handle_turn(page)
	presentation_show(slide_view)

def _pop_push_page(pop_pages, push_pages):
	def action():
		try:
			page = pop_pages.pop()
		except IndexError:
			return
		push_pages.append(current_page)
		_goto(page)
	return action


back    = _pop_push_page(past_pages, future_pages)
forward = _pop_push_page(future_pages, past_pages)

def goto_page(page):
	page = min(max(first_page, page), last_page)
	if page == current_page:
		return
	
	if future_pages and page == future_pages[-1]:
		forward()
	elif past_pages and page == past_pages[-1]:
		back()
	else:
		del future_pages[:]
		past_pages.append(current_page)
		_goto(page)


pages = list(range(page_count)) # pages index

frames = []      # frames index
frame_pages = [] # list of overlays by page
current_label = None
for page_number in range(page_count):
	page = pdf.pageAtIndex_(page_number)
	label = page.label()
	if label != current_label:
		# a new frame just started
		frames.append(page_number)
		current_label = label
	frame_pages.append(list(range(frames[-1], page_number+1)))

sections = [] # sections index
outline = pdf.outlineRoot()
if outline:
	for i in range(outline.numberOfChildren()):
		section = outline.childAtIndex_(i)
		destination = section.destination()
		sections.append(pdf.indexForPage_(destination.page()))

def _next(index):
	for page in index:
		if page > current_page:
			return page
	return current_page

def _prev(index):
	for page in reversed(index):
		if page < current_page:
			return page
	return current_page

def home_page():    goto_page(first_page)
def end_page():     goto_page(last_page)
def next_page():    goto_page(_next(pages))
def prev_page():    goto_page(_prev(pages))
def next_frame():   goto_page(_next(frames))
def prev_frame():   goto_page(_prev(frames))
def next_section(): goto_page(_next(sections))
def prev_section(): goto_page(_prev(sections))


# youtube redirection

YOUTUBE = 'www.youtube.com'
invidious = None

def redirect(url):
	if url and url.host() == YOUTUBE:
		global invidious
		if invidious is None:
			try:
				data, response, _ = NSURLConnection.sendSynchronousRequest_returningResponse_error_(
					NSURLRequest.requestWithURL_cachePolicy_timeoutInterval_(
						NSURL.URLWithString_('https://api.invidious.io/instances.json?sort_by=health'),
						NSURLRequestReloadIgnoringLocalCacheData,
						2
					), None, None
				)
				assert response.statusCode() == 200 # found
				import json
				invidious, _ = json.loads(bytearray(data))[0]
			except:
				pass
		s = url.absoluteString()
		if invidious:
			s = s.replace(YOUTUBE, invidious)
		url = NSURL.URLWithString_(s)
	return url


# movie annotations

player = AVPlayer.playerWithURL_(None)
nop_event = NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(
	NSEventTypeApplicationDefined, (0, 0), 0, 0., 0, None, 0, 0, 0
)

class PlayerItemObserver(NSObject):
	def observeValueForKeyPath_ofObject_change_context_(self, keyPath, item, change, context):
		assert type(item) == AVPlayerItem
		assert change["new"] != change["old"]
		assert change["new"] == item.status()
		item.removeObserver_forKeyPath_(self, "status")
		
		self.playable = item.status() == AVPlayerItemStatusReadyToPlay
		app.stop_(self)
		app.postEvent_atStart_(nop_event, True) # we are not in event thread
item_observer = PlayerItemObserver.alloc().init()


def get_movie(url):
	"""return a AVPlayerItem object from an url if possible/desirable"""
	if not (url and url.scheme() == "file"):
		return
	mimetype, _ = mimetypes.guess_type(url.absoluteString())
	if not (mimetype and any(mimetype.startswith(t) for t in ["video", "audio", "image/gif"])):
		return
	
	global restarted
	asset = AVAsset.assetWithURL_(url)
	player_item = AVPlayerItem.playerItemWithAsset_automaticallyLoadedAssetKeys_(
		asset,
		["playable",],
	)
	player_item.addObserver_forKeyPath_options_context_(
		item_observer, "status",
		NSKeyValueObservingOptionOld | NSKeyValueObservingOptionNew,
		None,
	)
	player.replaceCurrentItemWithPlayerItem_(player_item)
	app.run()
	restarted = True
	player.replaceCurrentItemWithPlayerItem_(None)
	
	if not item_observer.playable:
		return
	
	image_generator = AVAssetImageGenerator.assetImageGeneratorWithAsset_(asset)
	try:
		image_ref = _e(image_generator.copyCGImageAtTime_actualTime_error_(
			(0, 1, 1, 0), None, None,
		))
		poster = NSImage.alloc().initWithCGImage_size_(image_ref, (0, 0))
	except:
		poster = None
	return player_item, poster


# animations generated with the animate package

# this code is fragile: it relies on pdf and javascript naming conventions
# generated by the tex animate package:
# https://ctan.org/pkg/animate

animations_state = {}
autoplay_animations = defaultdict(list)
def parse_js(script, page_number):
	try:
		script = script.decode()
	except AttributeError:
		pass
	
	context = JSContext.alloc().init()
	context.evaluateScript_("""
		// stubbing getField and any other method by subsequent results
		const app = new Proxy({}, {
			get(target, prop, receiver) {
				return function(_) { return receiver; };
			}
		});
		getField = getOCGs = app.get;
		
		// stubbing javascript state expected by animate machinery
		var display = {
			hidden:  true,
			visible: true,
		};
		
		%(script)s
		
		// exposing global state names
		var i = Object.keys(this).filter(k => k.endsWith('_int'))[0];
		if(i != undefined) {
			var a = i.substring('a'.length, i.length-'_int'.length);
		} else { //arbitrary upper bound
			for(var a=0; a<100; a++){ if(this.hasOwnProperty('a'+a)) break; }
		}
		let p = 'a'+a;

		var fps, playing, next;
		if(this.hasOwnProperty(p)) { // handle animate prior to 20160826
			e = this[p];
			fps     = 1000/e.dt - 1e-6;
			playing = e.isPlaying;
			next    = e.actnNext;
		} else {
			fps     = this[p+'_fps'];
			playing = this[p+'_playing'];
			next    = this[p+'_gotoNext']
		}
	""" % {'script': script})
	assert context.exception() == None, context.exception()

	a = int(context.objectForKeyedSubscript_('a').toNumber())

	autoplay = context.objectForKeyedSubscript_('playing').toBool()
	if autoplay:
		autoplay_animations[page_number].append(a)
	fps = float(context.objectForKeyedSubscript_('fps').toNumber())
	loop = any(
		p in context.objectForKeyedSubscript_('next').toString()
		for p in ['playing', 'isPlaying']
	)

	animations_state[a] = (1 if autoplay else 0, fps, loop)


animations = {}
def prepare_animations(annotations):
	for k in annotations:
		if 'PlayPause' in k and k.replace('PlayPause', 'Play') in annotations or \
		   'PlayPause' not in k and 'Pause' in k:
			annot = annotations[k]
			annot.setValue_forAnnotationKey_(4, 'F')
			annot.setShouldDisplay_(False)
	
	a = 0
	while True:
		try:
			anim = annotations['anm%i' % a]
		except KeyError:
			break
		flags = anim.valueForAnnotationKey_('F')
		anim.setShouldDisplay_(False)
		frames = []
		i = 0
		while True:
			try:
				frame = annotations['%i.%i' % (a, i)]
			except KeyError:
				break
			frame.setValue_forAnnotationKey_(flags, 'F')
			if i > 0:
				frame.setShouldDisplay_(False)
			frames.append(frame)
			i += 1
		animations[a] = frames
		a += 1

class AnimationPlayer(NSObject):
	def play_(self, timer):
		a, step = timer.userInfo()
		advance_animation(a, step)
		refresher.refresh()

animation_player = AnimationPlayer.alloc().init()

animation_timer = None
def advance_animation(a, step=0, target=None):
	frames = animations[a]
	for current, f in enumerate(frames):
		if f.shouldDisplay(): break
	frames[current].setShouldDisplay_(False)
	
	if target is None:
		target = current + step
	
	step, fps, loop = animations_state[a]
	
	l = len(frames)
	if target >= l:  target = 0 if loop else -1
	elif target < 0: target = -1 if loop else 0
	frames[target].setShouldDisplay_(True)
	
	global animation_timer
	if animation_timer:
		animation_timer.invalidate()

	if step == 0:
		return
	if not loop and \
	   ((step < 0 and target == 0) or \
	    (step > 0 and target == -1)):
		d = {-1: 'Left', 1: 'Right'}[step]
		for w in ['%i.Pause%s', '%i.PlayPause%s']:
			key = w % (a, d)
			if key in widgets:
				handle_animation(widgets[key])
				break
		return
	
	animation_timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
		1./fps,
		animation_player, 'play:',
		(a, step), NO)


def toggle_play_pause(a, play):
	for d in ['Left', 'Right']:
		for p, v in [('Play', play), ('Pause', not play)]:
			try:
				w = widgets['%i.%s%s' % (a, p, d)]
			except KeyError:
				continue
			w.setShouldDisplay_(v)
	
def handle_animation(annotation):
	t = annotation.valueForAnnotationKey_('T')
	if t.startswith('btn@'):
		t = t[len('btn@'):].replace('@', '.')
	try:
		a, t = t.split('.')
		a = int(a)
	except: # not an animation
		return
	step, target = None, None
	
	if t in ['EndLeft', 'StepLeft', 'StepRight', 'EndRight']:
		step, target = {
			'EndLeft':   (None,  0),
			'EndRight':  (None, -1),
			'StepLeft':  (-1, None),
			'StepRight': ( 1, None),
		}[t]
		advance_animation(a, step, target)
	
	elif t in ['PlayLeft', 'PauseLeft', 'PauseRight', 'PlayRight']:
		step = {
			'PlayLeft':   -1,
			'PlayRight':   1,
			'PauseLeft':   0,
			'PauseRight':  0,
		}[t]
		_, fps, loop = animations_state[a]
		animations_state[a] = step, fps, loop
		advance_animation(a)
		toggle_play_pause(a, 'Pause' in t)
	
	elif t in ['PlayPauseLeft', 'PlayPauseRight']:
		step = {
			'PlayPauseLeft':  -1,
			'PlayPauseRight':  1,
		}[t]
		_step, fps, loop = animations_state[a]
		if _step == step:
			step = 0
		animations_state[a] = step, fps, loop
		advance_animation(a)
		
	elif t in ['Minus', 'Plus', 'Reset']:          pass
	else:
		advance_animation(a, 1)
	refresher.refresh()


# scanning annotations for notes, movies and animations #####################

def add_movie_pdfannotationlink(page_number, annot, movie):
	if type(movie) == CGPDFDictionaryRef:
		try:
			fs = cgpdf_get(movie, 'FS')
		except LookupError:
			movie_filename = os.path.join(TMP_DIR_PATH, os.path.basename(cgpdf_get(movie, 'F')))
			with open(movie_filename, 'bw') as movie_file:
				movie_file.write(cgpdf_get(movie, 'EF', 'F'))
			u = NSURL.fileURLWithPath_(movie_filename)
		else:
			u = NSURL.URLWithString_(cgpdf_get(movie, 'F'))
	else:
		u = url.URLByDeletingLastPathComponent().URLByAppendingPathComponent_(movie)
	rect = cgpdf_array2list(cgpdf_get(annot, 'Rect'))
	x0, y0, x1, y1 = rect
	pdf_annotation = PDFAnnotation.alloc().initWithBounds_forType_withProperties_(
		((x0, y0), (x1-x0, y1-y0)),
		'Link',
		None
	)
	pdf_annotation.setURL_(u)
	pdf.pageAtIndex_(page_number).addAnnotation_(pdf_annotation)


# low level annotation scanning for embedded data (media or javascript)

for page_number in range(_page_count):
	_page = CGPDFDocumentGetPage(_pdf, page_number+1)
	_dict = CGPDFPageGetDictionary(_page)
	try:
		_annotations = cgpdf_get(_dict, 'Annots')
	except LookupError:
		continue
	for annot in cgpdf_array2list(_annotations):
		subtype = cgpdf_get(annot, 'Subtype')
		if subtype == 'Movie':
			movie_filename = cgpdf_get(annot, 'Movie', 'F')
			add_movie_pdfannotationlink(page_number, annot, movie_filename)
		
		elif subtype in ['Screen', 'Widget']:
			try:
				po = cgpdf_get(annot, 'AA', 'PO')
			except LookupError:
				continue
			po_subtype = cgpdf_get(po, 'S')
			if po_subtype == 'JavaScript': # animate info?
				try:
					parse_js(cgpdf_get(po, 'JS'), page_number)
				except:
					pass
			elif po_subtype == 'Rendition': # movie15 style embedded movie?
				r = cgpdf_get(po, 'R')
				if cgpdf_get(r, 'S') != 'MR': continue
				c = cgpdf_get(r, 'C')
				if cgpdf_get(c, 'S') != 'MCD': continue
				movie = cgpdf_get(po, 'R', 'C', 'D')
				add_movie_pdfannotationlink(page_number, annot, movie)
		
		elif subtype == 'RichMedia': # media9 style embedded movie?
			content = cgpdf_get(annot, 'RichMediaContent')
			try:
				params = cgpdf_get(content, 'Configurations', 0, 'Instances', 0, 'Params', 'FlashVars')
				params = dict(
					param.split('=')
					for param in params.split('&') if param
				)
				source = params['source']
			except LookupError:
				source = None
			assets = iter(cgpdf_array2list(cgpdf_get(content, 'Assets', 'Names')))
			for asset_name in assets:
				movie = next(assets)
				if asset_name == source:
					break
			add_movie_pdfannotationlink(page_number, annot, movie)


# high level annotation handling

def annotations(page):
	return page.annotations() or []

pdf_notes = defaultdict(list)
movies = {}
widgets = {}
for page_number in range(page_count):
	page = pdf.pageAtIndex_(page_number)
	for annotation in annotations(page):
		annotation_type = annotation.type()
		if annotation_type == 'Text':
			annotation.setShouldDisplay_(False)
			pdf_notes[page_number].append(annotation.contents().replace('\r', '\n'))
		elif annotation_type == 'Link':
			movie = get_movie(annotation.URL())
			if movie:
				movies[annotation] = movie
		elif annotation_type == 'Widget':
			widgets[annotation.valueForAnnotationKey_('T')] = annotation
		elif annotation_type in ['Movie', 'Screen', 'FileAttachment', 'RichMedia']:
			annotation.setShouldDisplay_(False)
prepare_animations(widgets)


# beamer notes

def lines(selection):
	return [line.string() for line in selection.selectionsByLine() or []]

beamer_notes = defaultdict(list)
title_page = pdf.pageAtIndex_(0)
(x, y), (w, h) = title_page.boundsForBox_(kPDFDisplayBoxMediaBox)
ratio = w/h

if ratio > 7/3: # likely to be a two screens pdf
	# heuristic to guess template of note slide
	ratio /= 2
	w /= 2
	title = lines(title_page.selectionForRect_(((x, y), (w, h))))
	miniature = lines(title_page.selectionForRect_(((x+w+3*w/4, y+3*h/4), (w/4, h/4))))
	header = miniature and all( # miniature do not have navigation
		line in title
		for line in miniature
	)
	for page_number in range(page_count):
		page = pdf.pageAtIndex_(page_number)
		(x, y), (w, h) = page.boundsForBox_(kPDFDisplayBoxMediaBox)
		w /= 2
		page.setBounds_forBox_(((x, y), (w, h)), kPDFDisplayBoxCropBox)
		selection = page.selectionForRect_(((x+w, y), (w, 3*h/4 if header else h)))
		beamer_notes[page_number].append('\n'.join(lines(selection)))


# thumbnails

origin = 0
thumbnails = {}
for page_number in range(page_count):
	page = pdf.pageAtIndex_(page_number)
	_, (w, h) = page.boundsForBox_(kPDFDisplayBoxCropBox)
	width = MINIATURE_WIDTH-MINIATURE_MARGIN
	height = h*width/w
	thumbnail = page.thumbnailOfSize_forBox_((width, height), kPDFDisplayBoxCropBox)
	thumbnails[page_number] = (width, height, origin), thumbnail
	origin += height + MINIATURE_MARGIN
MINIATURES_HEIGHT = origin

drawings = defaultdict(list)
BOARD = -1
frame_pages.append([BOARD])


# page drawing ##############################################################

slide_bbox = NSAffineTransform.transform()
board_bbox = NSAffineTransform.transform()
cursor_location = NSZeroPoint

color_chooser = NSColorPanel.sharedColorPanel()
color_chooser.setLevel_(CGShieldingWindowLevel())
color_chooser.setMode_(NSColorPanelModeCrayon)
color_chooser.setColor_(NSColor.blackColor())
color_chooser.setShowsAlpha_(True)

def stroke(path, color=NSColor.blackColor(), outline=NSColor.whiteColor(), size=1):
	if outline and color.alphaComponent() >= 1.:
		outline.setStroke()
		path.setLineWidth_(size+1)
		path.stroke()
	color.setStroke()
	path.setLineWidth_(size)
	path.stroke()


def draw_page(page):
	NSEraseRect(page.boundsForBox_(kPDFDisplayBoxCropBox))
	page.drawWithBox_(kPDFDisplayBoxCropBox)
	
	for annotation in annotations(page):
		if not annotation in movies:
			continue
		bounds = annotation.bounds()
		
		_, poster = movies[annotation]
		if poster is None:
			continue
		
		if bounds.size.height < MIN_POSTER_HEIGHT:
			continue
		
		poster_size = poster.size()
		aspect_ratio = ((poster_size.width*bounds.size.height)/
		                (bounds.size.width*poster_size.height))
		if aspect_ratio < 1:
			dw = bounds.size.width * (1.-aspect_ratio)
			bounds.origin.x += dw/2.
			bounds.size.width -= dw
		else:
			dh = bounds.size.height * (1.-1./aspect_ratio)
			bounds.origin.y += dh/2.
			bounds.size.height -= dh
		
		poster.drawInRect_fromRect_operation_fraction_(
			bounds, NSZeroRect, NSCompositingOperationCopy, 1.
		)


# presentation ##############################################################

def draw_cursor(x, y, iw, ih):
	cursor_bounds = NSRect()
	W, H = CURSOR.size()
	cursor_bounds.size = (W/iw, H/ih)
	cursor_bounds.origin = x-X_hot/iw, y-(H-Y_hot)/ih
	CURSOR.drawInRect_fromRect_operation_fraction_(
		cursor_bounds, NSZeroRect, NSCompositingOperationSourceAtop, 1.
	)


NO_LIGHT, LASER, HIGH_LIGHT = range(3)

class SlideView(NSView):
	cursor_scale = 1.
	spotlight_radius = 20.
	show_cursor = False
	show_spotlight = NO_LIGHT
	hide_timer = None
	
	def drawRect_(self, rect):
		bounds = self.bounds()
		width, height = bounds.size
		
		NSRectFillUsingOperation(bounds, NSCompositingOperationClear)
		
		# current page
		page = pdf.pageAtIndex_(current_page)
		page_rect = page.boundsForBox_(kPDFDisplayBoxCropBox)
		_, (w, h) = page_rect
		r = min(width/w, height/h)
		
		NSGraphicsContext.saveGraphicsState()
		transform = NSAffineTransform.transform()
		transform.translateXBy_yBy_(width/2., height/2.)
		transform.scaleXBy_yBy_(r, r)
		transform.translateXBy_yBy_(-w/2., -h/2.)
		transform.concat()
		slide_bbox.concat()
		draw_page(page)
		for page in frame_pages[current_page]:
			for path, color, size in drawings[page]:
				stroke(path, color, size=size)
		
		x, y = cursor_location
		if self.show_spotlight:
			r = self.spotlight_radius*self.cursor_scale
			if self.show_spotlight == LASER:
				LASER_GRADIENT.drawFromCenter_radius_toCenter_radius_options_(
					cursor_location, 0.,
					cursor_location, r/4., 0
				)
			elif self.show_spotlight == HIGH_LIGHT:
				spotlight = NSBezierPath.bezierPathWithRect_(bounds)
				if spotlight.containsPoint_(cursor_location):
					focus = NSBezierPath.bezierPathWithOvalInRect_(((x-r, y-r), (2*r, 2*r)))
					stroke(focus)
					spotlight.appendBezierPath_(focus)
					spotlight.setWindingRule_(NSEvenOddWindingRule)
					NSColor.colorWithCalibratedWhite_alpha_(.5, .5).setFill()
					spotlight.fill()
		elif self.show_cursor:
			iw, ih = transform.transformSize_((1./self.cursor_scale, 1./self.cursor_scale))
			draw_cursor(x, y, iw, ih)
		
		self.transform = transform
		self.transform.invert()
		NSGraphicsContext.restoreGraphicsState()
	
	def showCursor(self):
		self.show_cursor = True
		self.setNeedsDisplay_(True)
		if self.hide_timer:
			self.hide_timer.invalidate()
		self.hide_timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
			5.,
			self, "hideCursor:",
			nil, NO)
	
	def hideCursor_(self, timer):
		self.show_cursor = False
		self.setNeedsDisplay_(True)
	
	def mouseUp_(self, event):
		if event.clickCount() < 2:
			return
		if presenter_view.isInFullScreenMode():
			toggle_fullscreen()
			return
		
		_fullscreen = presentation_window.styleMask() & NSWindowStyleMaskFullScreen
		if not _fullscreen:
			presentation_window.setStyleMask_(NSWindowStyleMaskResizable|NSWindowStyleMaskTitled)
		presentation_window.toggleFullScreen_(None)
		if _fullscreen:
			presentation_window.setStyleMask_(NSWindowStyleMaskResizable|NSWindowStyleMaskBorderless)


class BoardView(NSView):
	def initWithFrame_(self, frame):
		assert NSView.initWithFrame_(self, frame) == self
		self.setCanDrawConcurrently_(True)
		self.setBackgroundColor_(NSColor.whiteColor())
		return self

	def drawRect_(self, rect):
		_, (w, h) = bounds = self.bounds()
		NSEraseRect(bounds)

		for path, color, size in drawings[BOARD]:
			stroke(path, color, outline=None, size=size)

		x, y = cursor_location
		iw, ih = 1./slide_view.cursor_scale, 1./slide_view.cursor_scale
		draw_cursor(x, y, iw, ih)


class MovieView(NSView):
	def initWithFrame_(self, frame):
		assert NSView.initWithFrame_(self, frame) == self
		
		self.setWantsLayer_(True)
		player_layer = AVPlayerLayer.playerLayerWithPlayer_(player)
		player_layer.setFrame_(frame)
		self.setLayer_(player_layer)
		
		self.slider = NSSlider.alloc().initWithFrame_(((0, 5), (frame.size.width, 25)))
		self.slider.setTarget_(self)
		self.slider.setAction_("slide:")
		add_subview(self, self.slider, NSViewWidthSizable)
		
		return self
	
	def mouseDown_(self, event):
		if self.isPlaying():
			self.pause()
		else:
			self.play()
	
	def setHidden_(self, hidden):
		if self.isHidden():
			self.pause()
		return super(MovieView, self).setHidden_(hidden)
	
	def slide_(self, slider):
		self._pause()
		
		p = slider.doubleValue()
		(t, st, _, _) = player.currentTime()
		try:
			(d, sd, _, _) = player.currentItem().duration()
			t = int(p*(1.*d/sd)*st)
		except: # no current item
			return
		player.seekToTime_toleranceBefore_toleranceAfter_(
			(t, st, 1, 0), (1, st, 1, 0), (1, st, 1, 0))
		self.seekSlider_(player.currentTime())
	
	def stepByCount_(self, count):
		self._pause()
		player.currentItem().stepByCount_(count)
		self.seekSlider_(player.currentTime())
	
	def seekSlider_(self, time):
		(t, st, _, _) = time
		try:
			(d, sd, _, _) = player.currentItem().duration()
			p = (1.*t/st) / (1.*d/sd)
		except: # no current item
			return 0.
		self.slider.setDoubleValue_(p)
	
	def play(self):
		player.play()
		self.time_observer = player.addPeriodicTimeObserverForInterval_queue_usingBlock_(
			CMTimeMakeWithSeconds(0.1, NSEC_PER_SEC),
			None,
			self.seekSlider_
		)
	
	def loadItem_(self, player_item):
		player.replaceCurrentItemWithPlayerItem_(player_item)
	
	def _pause(self):
		player.pause()
		try:
			player.removeTimeObserver_(self.time_observer)
		except:
			pass

	def pause(self):
		self._pause()
		self.seekSlider_(player.currentTime())
	
	def isPlaying(self):
		return player.rate() > 0.



class VideoView(NSView):
	def initWithFrame_(self, frame):
		assert NSView.initWithFrame_(self, frame) == self
		_, (w, h) = frame
		self.w = w
		self.h = h
		self.session = AVCaptureSession.alloc().init()
		if self.session.canSetSessionPreset_(AVCaptureSessionPreset320x240):
			self.session.setSessionPreset_(AVCaptureSessionPreset320x240)
		self.setWantsLayer_(True)
		self.preview = AVCaptureVideoPreviewLayer.layerWithSession_(self.session)
		self.preview.setFrame_(frame)
		self.preview.setMasksToBounds_(True)
		self.preview.setCornerRadius_(15.)
		self.preview.setVideoGravity_(AVLayerVideoGravityResizeAspectFill)
		self.setLayer_(self.preview)
		self.setAlphaValue_(.75)
		return self
	
	_small = True
	def layout(self):
		_, (w, h) =  self.superview().frame()
		if self._small:
			x, y = w-self.w-20, 20
			w, h = self.w, self.h
		else:
			x, y = 20, 20
			w, h = w-40, h-40
		self.setFrame_(((x, y), (w, h)))

	def viewDidEndLiveResize(self):
		self.layout()
	
	def toggle_size(self):
		self._small = not self._small
		if self._small:
			alpha = .75
			gravity = AVLayerVideoGravityResizeAspectFill
		else:
			alpha = 1.
			gravity = AVLayerVideoGravityResizeAspect
		self.setAlphaValue_(alpha)
		self.preview.setVideoGravity_(gravity)
		self.layout()
	
	
	device = None
	def choose_device(self):
		devices = AVCaptureDevice.devicesWithMediaType_(AVMediaTypeVideo)
		try:
			device, = devices
		except ValueError:
			toggle_fullscreen(fullscreen=False)
			alert = NSAlert.alloc().init()
			alert.setIcon_(ICON)
			alert.setMessageText_("Choose video device")
			alert.setInformativeText_("The following devices are available:")
			popup = NSPopUpButton.alloc().initWithFrame_pullsDown_(((0, 0), (200, 25)), False)
			for device in devices:
				popup.addItemWithTitle_(device.localizedName())
			alert.setAccessoryView_(popup)
			alert.runModal()
			device = devices[popup.indexOfSelectedItem()]
		return device
	
	def start(self, switch_device=False):
		if self.session.isRunning():
			self.stop()
		if switch_device or self.device is None:
			self.device = self.choose_device()
		capture_input = _e(AVCaptureDeviceInput.deviceInputWithDevice_error_(self.device, None))
		if self.session.canAddInput_(capture_input):
			self.session.addInput_(capture_input)
			self.session.startRunning()
	
	def stop(self):
		if not self.session.isRunning():
			return
		self.session.stopRunning()
		for input in self.session.inputs():
			self.session.removeInput_(input)
	
	def setHidden_(self, hidden):
		if hidden == False:
			if AVCaptureDevice.respondsToSelector_("authorizationStatusForMediaType:"):
				authorization = AVCaptureDevice.authorizationStatusForMediaType_(AVMediaTypeVideo)
			else:
				authorization = AVAuthorizationStatusAuthorized
			if authorization == AVAuthorizationStatusAuthorized:
				self.start()
			elif authorization == AVAuthorizationStatusNotDetermined:
				AVCaptureDevice.requestAccessForMediaType_completionHandler_(
					AVMediaTypeVideo,
					self.requestAccessHandler_,
				)
				pass
			else:
				alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
					"Access to Camera denied",
					"Ok", nil, nil,
					"You may want to grant access through the Security preference panel."
				)
				alert.setIcon_(ICON)
				button = alert.runModal()
				self.requestAccessHandler_(False)
		else:
			self.stop()
		return super(VideoView, self).setHidden_(hidden)
	
	def requestAccessHandler_(self, r):
		self.performSelectorOnMainThread_withObject_waitUntilDone_('setHidden:', nil if r else YES, False)


# presenter view ############################################################

IDLE, BBOX, SELECT, CLIC, MIN_CLIC, MIN_SCROLL, DRAW, DRAG = range(8)

def hasModifiers(event, mask):
	return (event.modifierFlags() & mask) == mask

def transform_rect(transform, rect):
	origin, size = rect
	return (transform.transformPoint_(origin), transform.transformSize_(size))

class PresenterView(NSView):
	transform = NSAffineTransform.transform()
	duration = presentation_duration * 60.
	absolute_time = True
	elapsed_duration = 0
	start_time = time.time()
	duration_change_time = 0
	show_help = True
	annotation_state = None
	notes_scale = .75
	target_page = ""
	miniature_origin = 0
	page_state = None
	page = None
	state = IDLE
	selection_rect = NSZeroRect
	selection = []
	preview_page = None
	
	
	def draw_miniatures(self):
		_, (width, height) = self.bounds()
		x = width - MINIATURE_WIDTH
		width = MINIATURE_WIDTH-MINIATURE_MARGIN
		
		if self.page_state != current_page: # ensure current page in view when page changed
			self.page_state = current_page
			(_, h, o), _ = thumbnails[current_page]
			self.miniature_origin = min(o-MINIATURE_MARGIN, self.miniature_origin)
			self.miniature_origin = max(self.miniature_origin, o+h+MINIATURE_MARGIN-height)
		
		self.miniature_origin = min(MINIATURES_HEIGHT-height, self.miniature_origin)
		self.miniature_origin = max(self.miniature_origin, -MINIATURE_MARGIN)
		
		for i in range(page_count):
			(w, h, o), image = thumbnails[i]
			y = self.miniature_origin+height-o-h
			if y < -h:
				break
			if y > height:
				continue
			image.drawInRect_fromRect_operation_fraction_(
				((x, y), (w, h)), NSZeroRect, NSCompositingOperationCopy, 1.
			)
			if i == current_page:
				NSColor.yellowColor().setFill()
				NSFrameRectWithWidth(((x, y), (w, h)), 2)
			elif i == self.preview_page or \
			     (self.preview_page is None and i == current_page+1):
				NSColor.lightGrayColor().setFill()
				NSFrameRectWithWidth(((x, y), (w, h)), 2)
			
			page_number = _s("%s" % (i+1,))
			attr = {
				NSFontAttributeName:            NSFont.labelFontOfSize_(11),
				NSForegroundColorAttributeName: NSColor.whiteColor(),
				NSParagraphStyleAttributeName:  right_align,
			}
			page_number.drawInRect_withAttributes_(((x-52, y+h-12), (50, 15)), attr)
	
	
	def drawRect_(self, rect):
		bounds = self.bounds()
		width, height = bounds.size
		width -= MINIATURE_WIDTH
		
		margin = width / 20.
		current_width = (width-3*margin)*2/3.
		font_size = margin/2.
		
		# current
		self.page = pdf.pageAtIndex_(current_page)
		if board_view.isHidden():
			page_rect = self.page.boundsForBox_(kPDFDisplayBoxCropBox)
			page = current_page
		else:
			page_rect = board_view.bounds()
			page = BOARD
		_, (w, h) = page_rect
		r = current_width/w
		current_height = h*r
		
		NSGraphicsContext.saveGraphicsState()
		transform = NSAffineTransform.transform()
		transform.translateXBy_yBy_(margin, height-1.5*margin)
		transform.scaleXBy_yBy_(r, r)
		transform.translateXBy_yBy_(0., -h)
		transform.concat()
		
		NSGraphicsContext.saveGraphicsState()
		
		if page == BOARD:
			bbox = board_bbox
			bbox.concat()
			NSEraseRect(page_rect)
			_, (w, h) = page_rect
			lines = NSBezierPath.bezierPath()
			y = 0.
			while y < h:
				y += 50
				lines.moveToPoint_((0, h-y))
				lines.lineToPoint_((w, h-y))
			x = 0.
			while x < w:
				x += 50
				lines.moveToPoint_((x, 0))
				lines.lineToPoint_((x, h))
			NSColor.grayColor().setStroke()
			lines.stroke()

		else:
			bbox = slide_bbox
			bbox.concat()
			draw_page(self.page)

			it = NSAffineTransform.alloc().initWithTransform_(transform)
			it.prependTransform_(bbox)
			it.invert()
			icon_size = it.transformSize_(FULL_SCREEN.size())
			
			# links and movies
			NSColor.blueColor().setFill()
			for annotation in annotations(self.page):
				bounds = annotation.bounds()
				if annotation.type() in ['Link', 'Widget'] and annotation.shouldDisplay():
					NSFrameRectWithWidth(bounds, .5)

				if annotation in movies:
					_, poster = movies[annotation]
					if poster is None:
						continue
					if bounds.size.height < MIN_POSTER_HEIGHT:
						continue
					
					rect = ((bounds.origin.x+bounds.size.width-icon_size.width-3, bounds.origin.y+bounds.size.height/6+3), icon_size)
					NSColor.colorWithCalibratedWhite_alpha_(0., 0.5).setFill()
					NSRectFillUsingOperation(rect, NSCompositingOperationDarken)
					NSColor.whiteColor().setFill()
					FULL_SCREEN.drawInRect_fromRect_operation_fraction_(
						rect,
						NSZeroRect,
						NSCompositingOperationSourceAtop,
						1.
					)

		for p in frame_pages[page]:
			for path, color, size in drawings[p]:
				stroke(
					path, color,
					outline=None if (path, color, size) not in self.selection else NSColor.yellowColor(),
					size=size
				)

		self.transform = transform
		self.transform.prependTransform_(bbox)
		self.resetCursorRects()
		self.transform.invert()

		_, s = self.transform.transformSize_((0, 1))
		NSColor.grayColor().setFill()
		NSFrameRectWithWidth(self.selection_rect, s)
		
		NSGraphicsContext.restoreGraphicsState()
		
		# screen border & cropping
		NSColor.grayColor().setFill()
		NSFrameRect(page_rect)

		# video view proxy
		if not video_view.isHidden():
			NSColor.colorWithCalibratedWhite_alpha_(.25, .25).setFill()
			rect = video_view.frame()
			if page == BOARD:
				rect = transform_rect(board_bbox, rect)
			else:
				rect = transform_rect(slide_view.transform, rect)
			NSRectFillUsingOperation(rect, NSCompositingOperationSourceAtop)

		NSGraphicsContext.restoreGraphicsState()
		NSRectFillUsingOperation(((0, 0), (margin, height)), NSCompositingOperationClear)
		NSRectFillUsingOperation(((margin, height-1.5*margin), (width+MINIATURE_WIDTH-margin, 1.5*margin)), NSCompositingOperationClear)
		NSRectFillUsingOperation(((margin+r*w, 0), (width+MINIATURE_WIDTH-margin+r*w, height)), NSCompositingOperationClear)
		NSRectFillUsingOperation(((0, 0), (width+MINIATURE_WIDTH, height-1.5*margin-r*h)), NSCompositingOperationClear)
		
		if self.state == DRAW:
			return
		
		# time
		now = time.time()
		if now - self.duration_change_time <= 1: # duration changed, display it
			clock = time.gmtime(self.duration)
		elif self.absolute_time:
			clock = time.localtime(now)
		else:
			running_duration = now - self.start_time + self.elapsed_duration
			clock = time.gmtime(abs(self.duration - running_duration))
		clock = _s(time.strftime("%H:%M:%S", clock))
		clock.drawAtPoint_withAttributes_((margin, height-1.4*margin), {
			NSFontAttributeName:            NSFont.labelFontOfSize_(margin),
			NSForegroundColorAttributeName: NSColor.whiteColor(),
		})
		app.dockTile().setBadgeLabel_(clock)
		
		# page number
		if self.target_page:
			page_number = _s("goto %s/%s" % (
				self.target_page, page_count))
		else:
			page_number = _s("(%s) %s/%s" % (
				self.page.label(), current_page+1, page_count))
		attr = {
			NSFontAttributeName:            NSFont.labelFontOfSize_(font_size),
			NSForegroundColorAttributeName: NSColor.whiteColor(),
			NSParagraphStyleAttributeName:  right_align,
		}
		tw, _ = page_number.sizeWithAttributes_(attr)
		page_number.drawInRect_withAttributes_(((margin+current_width-500,
		                                         height-1.4*margin), (500, font_size*1.2)), attr)
		
		if page in durations or page in autoplay_animations:
			PLAY.drawAtPoint_fromRect_operation_fraction_(
				(margin+current_width-20, height-1.5*margin-18),
				NSZeroRect,
				NSCompositingOperationExclusion, .5 if _auto_turn else 1.
			)

		# notes
		note = _s("".join(
			"\n\n".join(notes[current_page])
			for notes in [pdf_notes, beamer_notes]
		))
		note.drawInRect_withAttributes_(
			((margin, font_size), (current_width, height-current_height-2.5*margin)),
			{
				NSFontAttributeName:            NSFont.labelFontOfSize_(font_size*self.notes_scale),
				NSForegroundColorAttributeName: NSColor.whiteColor(),
			}
		)
		
		
		# help
		if self.show_help:
			attr = {
				NSFontAttributeName:            NSFont.labelFontOfSize_(11),
				NSForegroundColorAttributeName: NSColor.whiteColor(),
				NSParagraphStyleAttributeName:  right_align,
			}
			for i, (k, v) in enumerate(reversed(HELP)):
				_s(k).drawInRect_withAttributes_(
					((margin+current_width+10, i*15+5), (65, 14)),
					attr
				)
				_s(v).drawAtPoint_withAttributes_( # drawAtPoint ignores right_align
					(margin+current_width+90, i*15+5),
					attr
				)
		
		
		# thumbnails
		self.draw_miniatures()
		
		
		# next page or board
		if self.preview_page != None:
			next_page = pdf.pageAtIndex_(self.preview_page)
		elif current_page < last_page:
			next_page = pdf.pageAtIndex_(current_page+1)
		else:
			return
		
		page_rect = next_page.boundsForBox_(kPDFDisplayBoxCropBox)
		_, (w, h) = page_rect
		r = current_width/2./w
		
		NSGraphicsContext.saveGraphicsState()
		transform = NSAffineTransform.transform()
		transform.translateXBy_yBy_(2*margin+current_width, height-1.5*margin)
		transform.scaleXBy_yBy_(r, r)
		transform.translateXBy_yBy_(0., -h)
		transform.concat()
		
		NSEraseRect(page_rect)
		next_page.drawWithBox_(kPDFDisplayBoxCropBox)

		
		NSColor.colorWithCalibratedWhite_alpha_(.25, .25).setFill()
		NSRectFillUsingOperation(page_rect, NSCompositingOperationSourceAtop)
		
		ibbox = NSAffineTransform.alloc().initWithTransform_(slide_bbox)
		ibbox.invert()
		ibbox.concat()
		NSColor.grayColor().setFill()
		_, s = slide_bbox.transformSize_((0, 2))
		NSFrameRectWithWidth(page_rect, s)
		NSGraphicsContext.restoreGraphicsState()
	
	
	def resetCursorRects(self):
		# updates rectangles only if needed (so that tooltip timeouts work)
		if self.page is None:
			return
		
		annotation_state = (self.transform.transformStruct(), current_page, board_view.isHidden())
		if self.annotation_state == annotation_state:
			return
		self.annotation_state = annotation_state
		
		# reset cursor rects and tooltips
		self.discardCursorRects()
		self.removeAllToolTips()
		
		if not board_view.isHidden():
			return
		
		for i, annotation in enumerate(annotations(self.page)):
			if annotation.type() not in ['Link', 'Widget']:
				continue
			if not annotation.shouldDisplay():
				continue
			
			rect = transform_rect(self.transform, annotation.bounds())
			self.addCursorRect_cursor_(rect, NSCursor.pointingHandCursor())
			self.addToolTipRect_owner_userData_(rect, self, i)
	
	
	def view_stringForToolTip_point_userData_(self, view, tag, point, data):
		annotation = annotations(self.page)[data]
		return annotation.toolTip() or ""
	
	def zoomAt_by_(self, point, percent):
		bbox = slide_bbox if board_view.isHidden() else board_bbox
		bbox.translateXBy_yBy_(point.x, point.y)
		bbox.scaleBy_(exp(percent*0.01))
		bbox.translateXBy_yBy_(-point.x, -point.y)
	
	def keyDown_(self, event):
		def send(c): # resend event with modified character
			app.sendEvent_(NSEvent.keyEventWithType_location_modifierFlags_timestamp_windowNumber_context_characters_charactersIgnoringModifiers_isARepeat_keyCode_(
				event.type(), event.locationInWindow(), event.modifierFlags(), event.timestamp(), event.windowNumber(), event.context(),
				c, c, event.isARepeat(), ord(c)))
		
		c = event.characters()
		
		if hasModifiers(event, NSCommandKeyMask):
			c = event.charactersIgnoringModifiers()
			if c in "+=-_0)i": # slides scale
				if not movie_view.isHidden():
					presentation_show()
				if c == '=': c = '+'
				if c == '_': c = '-'
				if c == '+':
					self.zoomAt_by_(cursor_location,  5)
				elif c == '-':
					self.zoomAt_by_(cursor_location, -5)
				else: # reset bbox to identity
					if board_view.isHidden():
						global slide_bbox
						slide_bbox = NSAffineTransform.transform()
					else:
						global board_bbox
						board_bbox = NSAffineTransform.transform()
		
		if hasModifiers(event, NSControlKeyMask | NSCommandKeyMask):
			c = event.charactersIgnoringModifiers()
			if c not in 'f': # only handle cmd+ctrl+f as f for now
				return
		
		if c == 'q': # quit
			app.terminate_(self)
		
		elif c == 'r': # relaunch
			exit_relaunch(url.path(), current_page)
		
		elif c in "0123456789" + CR + DEL:
			if c == '0' and not self.target_page: # skip leading 0
				send(')')                         # and rather change zoom
				return
			if c == CR:
				if self.target_page:
					goto_page(int(self.target_page)-1)
				self.target_page = ''
			elif c == DEL:
				if self.target_page:
					self.target_page = self.target_page[:-1]
				else:
					page = current_page if board_view.isHidden() else BOARD
					if self.selection:
						for path in self.selection:
							try:
								drawings[page].remove(path)
							except ValueError:
								continue
						self.selection = []
					else:
						drawings[page] = drawings[page][:-1]
			else:
				self.target_page += c
		
		elif c == ESC: # esc
			toggle_fullscreen(fullscreen=False)
		
		elif c == NSF5FunctionKey:
			toggle_fullscreen(fullscreen=True)
		
		elif c == 'x':
			global _switched_screens
			_switched_screens = not _switched_screens
			toggle_fullscreen()
			toggle_fullscreen()
		
		elif c == 'h':
			app.hide_(app)
		
		elif c == '?':
			self.show_help = not self.show_help
		
		elif c == ' ': # play/pause video
			if movie_view.isHidden(): # or...
				if current_page in durations or current_page in autoplay_animations:
					toggle_auto_turn() # toggle auto page turn
				else:
					send('t')          # or toggle timer
				return
			
			if movie_view.isPlaying():
				movie_view.pause()
			else:
				movie_view.play()
		
		elif c in "<>": # movie navigation
			step = 1 if c == '>' else -1
			if movie_view.isHidden():
				for a in annotations(self.page):
					if a.type() != 'Widget': continue
					k = a.valueForAnnotationKey_('T')
					if k.startswith('anm'):
						a = int(k[len('anm'):])
						advance_animation(a, step)
						break
			else:
				movie_view.stepByCount_(step)
		
		elif c == 't': # toggle clock/timer
			self.absolute_time = not self.absolute_time
			now = time.time()
			if self.absolute_time:
				self.elapsed_duration += (now - self.start_time)
			else:
				self.start_time = now
		
		elif c in "z[]{}": # timer management
			self.start_time = time.time()
			self.elapsed_duration = 0
			
			self.duration += {
				'{': -600,
				'[':  -60,
				'z':    0,
				']':   60,
				'}':  600,
			}[c]
			self.duration = max(0, self.duration)
			self.duration_change_time = time.time()
		
		elif c in "+=-_0)": # notes or web view scale
			if c == '=': c = '+'
			if c == '_': c = '-'
			
			if web_view.isHidden(): # scaling notes
				if c == '+':
					self.notes_scale *= 1.1
				elif c == '-':
					self.notes_scale /= 1.1
				else:
					self.notes_scale = 1.
			else:                   # scaling web view
				magnification = web_view.magnification()
				if c == '+':
					magnification *= 1.1
				elif c == '-':
					magnification /= 1.1
				else:
					magnification = 1.
				web_view.setMagnification_centeredAtPoint_(magnification, (0., 0.))
		
		elif c in "pP":
			if c == 'p':
				slide_view.cursor_scale /= 1.5
			else:
				slide_view.cursor_scale *= 1.5
			slide_view.showCursor()
		
		elif c == 'l':
			slide_view.show_spotlight = (slide_view.show_spotlight + 1) % 3
			slide_view.showCursor()
		
		elif c == 'c': # choose color
			if not color_chooser.isVisible():
				color_chooser.orderFront_(None)
			else:
				color_chooser.orderOut_(None)
		
		elif c == 'e': # erase annotation
			page = current_page if board_view.isHidden() else BOARD
			if self.selection:
				for path in self.selection:
					try:
						drawings[page].remove(path)
					except ValueError:
						continue
				self.selection = []
			else:
				for end_frame in frames:
					if end_frame > page:
						break
				for p in range(page, end_frame):
					try:
						del drawings[p]
					except KeyError:
						pass
		
		elif c == 'V': # toggle video size
			video_view.toggle_size()
		
		else:
			actions = {
				'f':                     toggle_fullscreen,
				'.':                     toggle_black_view,
				'b':                     toggle_board_view,
				'w':                     toggle_web_view,
				'm':                     toggle_movie_view,
				'v':                     toggle_video_view,
				's':                     presentation_show,
				NSLeftArrowFunctionKey:  prev_page,
				NSUpArrowFunctionKey:    prev_page,
				NSPageUpFunctionKey:     prev_page,
				NSPrevFunctionKey:       prev_page,
				NSRightArrowFunctionKey: next_page,
				NSDownArrowFunctionKey:  next_page,
				NSPageDownFunctionKey:   next_page,
				NSNextFunctionKey:       next_page,
				NSHomeFunctionKey:       home_page,
				NSEndFunctionKey:        end_page,
			}
			if hasModifiers(event, NSCommandKeyMask):
				actions.update({
					NSLeftArrowFunctionKey:  back,
					NSRightArrowFunctionKey: forward,
					NSUpArrowFunctionKey:    prev_frame,
					NSDownArrowFunctionKey:  next_frame,
					NSPageUpFunctionKey:     prev_section,
					NSPageDownFunctionKey:   next_section,
				})
			action = actions.get(c, nop)
			action()
		
		refresher.refresh()
	
	
	# interaction

	def inMiniaturesAt_(self, point):
		_, (width, height) = self.bounds()
		ex, ey = point
		return (0 <= ey <= height) and (width - MINIATURE_WIDTH <= ex <= width)
	
	def pageAt_(self, point):
		_, (_, height) = self.bounds()
		ex, ey = point
		for i in range(page_count):
			(_, h, o), _ = thumbnails[i]
			if ey + h + MINIATURE_MARGIN > self.miniature_origin-o+height:
				break
		return i
	
	
	def startPathOnPage_(self, page):
		self.path = NSBezierPath.bezierPath()
		self.path.setLineCapStyle_(NSRoundLineCapStyle)
		self.path.setLineJoinStyle_(NSRoundLineJoinStyle)
		self.path.moveToPoint_(self.press_location)
		self.path.lineToPoint_(cursor_location)
		drawings[page].append((
			self.path, color_chooser.color(),
			slide_view.cursor_scale*(3 if page == BOARD else 1)
		))
	
	def transformSelectionBy_(self, t):
		if board_view.isHidden():
			page = current_page
			view = slide_view
		else:
			page = BOARD
			view = board_view
		for path in drawings[page]:
			if path not in self.selection:
				continue
			b, _, _ = path
			b.transformUsingAffineTransform_(t)
		refresher.refresh([view])
	
	def click(self):
		if not video_view.isHidden():
			rect = video_view.frame()
			rect = transform_rect(slide_view.transform, rect)
			if NSPointInRect(self.press_location, rect):
				video_view.start(switch_device=True)
				return

		annotation = self.page.annotationAtPoint_(self.press_location)
		if annotation is None:
			next_page()
			return
		
		if annotation.type() not in ['Link', 'Widget']:
			return
		
		if annotation in movies:
			player_item, _ = movies[annotation]
			it = NSAffineTransform.alloc().initWithTransform_(self.transform)
			it.prependTransform_(slide_bbox)
			it.invert()
			icon_size = it.transformSize_(FULL_SCREEN.size())
			origin, size = annotation.bounds()
			origin.x += size.width-icon_size.width-3
			origin.y += size.height/6+3
			slide_frame = slide_view.frame()
			if size.height < MIN_POSTER_HEIGHT or \
			   NSPointInRect(self.press_location, (origin, icon_size)) and \
			   movie_view.frame() != slide_frame:
				rect = slide_frame
			else:
				it = NSAffineTransform.alloc().initWithTransform_(slide_view.transform)
				it.invert()
				it.prependTransform_(slide_bbox)
				rect = transform_rect(it, annotation.bounds())
			movie_view.setFrame_(rect)
			presentation_show(movie_view)
			movie_view.loadItem_(player_item)
			return
		
		action = annotation.mouseUpAction()

		if annotation.type() == 'Widget':
			handle_animation(annotation)
			return
		
		destination = annotation.destination()
		url = annotation.URL()
		
		if type(action) == PDFActionNamed:
			action_name = action.name()
			action = {
				kPDFActionNamedNextPage:     next_page,
				kPDFActionNamedPreviousPage: prev_page,
				kPDFActionNamedFirstPage:    home_page,
				kPDFActionNamedLastPage:     end_page,
				kPDFActionNamedGoBack:       back,
				kPDFActionNamedGoForward:    forward,
#				kPDFActionNamedGoToPage:     nop,
#				kPDFActionNamedFind:         nop,
#				kPDFActionNamedPrint:        nop,
			}.get(action_name, nop)
			action()
		
		elif destination:
			goto_page(pdf.indexForPage_(destination.page()))
		
		elif url:
			if not use_youtube:
				url = redirect(url)
			web_view.loadRequest_(NSURLRequest.requestWithURL_(url))

	delta = 0.
	def scrollWheel_(self, event):
		location = event.locationInWindow()
		center = self.transform.transformPoint_(location)
		if hasModifiers(event, NSCommandKeyMask):
			if not movie_view.isHidden():
				presentation_show()
			self.zoomAt_by_(center, event.deltaY())
		elif self.inMiniaturesAt_(location):
			if not event.phase(): # mouse vs. gesture
				(_, h, _), _ = thumbnails[current_page]
				h += MINIATURE_MARGIN
				if event.scrollingDeltaY() < 0:
					h = -h
				self.miniature_origin -= h
			else:
				self.miniature_origin -= event.scrollingDeltaY()
		elif self.selection:
			t = NSAffineTransform.transform()
			t.translateXBy_yBy_(center.x, center.y)
			t.scaleBy_(exp(event.deltaY()*0.05))
			t.translateXBy_yBy_(-center.x, -center.y)
			self.transformSelectionBy_(t)
		elif slide_view.show_spotlight:
			slide_view.spotlight_radius *= exp(event.deltaY()*0.05)
			refresher.refresh([slide_view])
		else:
			self.delta += event.deltaY()
			if abs(self.delta) < 1:
				return
			if self.delta < 0.:
				next_page()
			elif self.delta > 0.:
				prev_page()
			self.delta = 0
			refresher.refresh([slide_view])
		refresher.refresh([self])
	
	def mouseDown_(self, event):
		if color_chooser.isVisible():
			color_chooser.orderFront_(None)
		assert self.state == IDLE
		location = event.locationInWindow()
		self.press_location = self.transform.transformPoint_(location)
		if self.inMiniaturesAt_(location):
			self.state = MIN_CLIC
		elif hasModifiers(event, NSCommandKeyMask): # editing bbox
			if not movie_view.isHidden():
				presentation_show()
			self.state = BBOX
		elif hasModifiers(event, NSAlternateKeyMask): # starting a selection
			self.state = SELECT
		elif (
			hasModifiers(event, NSShiftKeyMask) or
			event.subtype() == NSEventSubtypeTabletPoint or
			not board_view.isHidden()
		):
			if self.selection:
				self.state = DRAG
			else:
				page = current_page if board_view.isHidden() else BOARD
				self.startPathOnPage_(page)
				self.state = DRAW
		else:
			self.state = CLIC
	
	def mouseMoved_(self, event):
		global cursor_location
		location = event.locationInWindow()
		cursor_location = self.transform.transformPoint_(location)
		slide_view.showCursor()
		if not board_view.isHidden(): # no real time drawing for slide because it's too slow
			refresher.refresh([board_view])
		
		if self.inMiniaturesAt_(location):
			i = self.pageAt_(location)
			if i != self.preview_page:
				self.preview_page = i
				refresher.refresh([self])
		else:
			if self.preview_page != None:
				self.preview_page = None
				refresher.refresh([self])

	
	def mouseDragged_(self, event):
		location = self.transform.transformPoint_(event.locationInWindow())
		if self.state in [MIN_CLIC, CLIC] and \
		   hypot(location.x-self.press_location.x, location.y-self.press_location.y) < 5:
			return

		global cursor_location
		dx, dy = location.x-cursor_location.x, location.y-cursor_location.y
		cursor_location = location

		if self.state == MIN_CLIC:
			self.state = MIN_SCROLL
		elif self.state == MIN_SCROLL:
			self.miniature_origin -= event.deltaY()
		elif self.state == SELECT:
			self.selection_rect = NSUnionRect((self.press_location, (1, 1)), (cursor_location, (1, 1)))
		elif self.state == BBOX:
			delta = self.transform.transformSize_((event.deltaX(), -event.deltaY()))
			bbox = slide_bbox if board_view.isHidden() else board_bbox
			bbox.translateXBy_yBy_(delta.width, delta.height)
		elif self.state == CLIC:
			page = current_page if board_view.isHidden() else BOARD
			self.startPathOnPage_(page)
			self.state = DRAW
		elif self.state == DRAW:
			self.path.lineToPoint_(cursor_location)
			if not board_view.isHidden(): # no real time drawing for slide because it's too slow
				refresher.refresh([board_view])
		elif self.state == DRAG:
			t = NSAffineTransform.transform()
			t.translateXBy_yBy_(dx, dy)
			self.transformSelectionBy_(t)
		self.display()
	
	def mouseUp_(self, event):
		if self.state == MIN_CLIC:
			i = self.pageAt_(event.locationInWindow())
			goto_page(i)
		elif self.state == CLIC:
			self.click()
		elif self.state == SELECT:
			self.selection = [
				(path, color, size)
				for path, color, size in drawings[current_page if board_view.isHidden() else BOARD]
				if NSContainsRect(self.selection_rect, path.bounds()) or NSPointInRect(path.currentPoint(), self.selection_rect)
			]
			self.selection_rect = NSZeroRect
		slide_view.showCursor()
		self.state = IDLE
		refresher.refresh()
	
	def rightMouseUp_(self, event):
		prev_page()
		refresher.refresh()


# application delegate ######################################################

# menus

def add_item(menu, title, action, key="", modifiers=NSCommandKeyMask, target=app):
	menu_item = menu.addItemWithTitle_action_keyEquivalent_(
		NSString.localizedStringWithFormat_(' '.join(("%@",) * len(title)), *(_s(s) for s in title)),
		action, key)
	menu_item.setKeyEquivalentModifierMask_(modifiers)
	menu_item.setTarget_(target)
	return menu_item

def setup_menu(delegate):
	main_menu = NSMenu.alloc().initWithTitle_("MainMenu")
	
	application_menuitem = main_menu.addItemWithTitle_action_keyEquivalent_("Application", None, ' ')
	application_menu = NSMenu.alloc().initWithTitle_("Application")
	
	add_item(application_menu, ["About", NAME], "about:", target=delegate)
	add_item(application_menu, ["Check for updates…"], "update:", target=delegate)
	application_menu.addItem_(NSMenuItem.separatorItem())
	add_item(application_menu, ["Hide", NAME], "hide:", 'h')
	add_item(application_menu, ["Hide Others"], "hideOtherApplications:", 'h', NSCommandKeyMask | NSAlternateKeyMask)
	add_item(application_menu, ["Show All"], "unhideAllApplications:")
	application_menu.addItem_(NSMenuItem.separatorItem())
	add_item(application_menu, ["Quit", NAME], "terminate:", 'q')
	main_menu.setSubmenu_forItem_(application_menu, application_menuitem)

	view_menuitem = main_menu.addItemWithTitle_action_keyEquivalent_("View", None, ' ')
	view_menu = NSMenu.alloc().initWithTitle_("View")
	add_item(view_menu, ["Enter Full Screen"], "fullScreen:", 'f', NSCommandKeyMask | NSControlKeyMask, target=delegate)
	main_menu.setSubmenu_forItem_(view_menu, view_menuitem)
	
	app.setMainMenu_(main_menu)
	
	app.setApplicationIconImage_(ICON)


# notifications

class UserNotificationCenterDelegate(NSObject):
	def userNotificationCenter_didReceiveNotificationResponse_withCompletionHandler_(self, center, response, handler):
		NSWorkspace.sharedWorkspace().openURL_(NSURL.URLWithString_(HOME))
		handler()
notification_delegate = UserNotificationCenterDelegate.alloc().init()
notification_center = UNUserNotificationCenter.currentNotificationCenter()
notification_center.setDelegate_(notification_delegate)

def completion_handler(error):
	if error: NSLog("%@", error)

def authorizationGranted_Error_(granted, error):
	if not granted:
		return
	version = get_version()
	if version in [VERSION, None]:
		return
	notification = UNMutableNotificationContent.alloc().init()
	notification.setTitle_(_s(NAME))
	notification.setSubtitle_('A new version (%s) is available' % version)
	request = UNNotificationRequest.requestWithIdentifier_content_trigger_('.'.join([ID, version]), notification, None)
	notification_center.addNotificationRequest_withCompletionHandler_(request, completion_handler)
	
def notify_update():
	if user_defaults.boolForKey_(NO_NOTIFY):
		return
	notification_center.requestAuthorizationWithOptions_completionHandler_(
		UNAuthorizationOptionProvisional,
		authorizationGranted_Error_,
	)


def get_version():
	try:
		data, response, _ = NSURLConnection.sendSynchronousRequest_returningResponse_error_(
			NSURLRequest.requestWithURL_cachePolicy_timeoutInterval_(
				NSURL.URLWithString_(HOME + "releases/version.txt?v=%s"%VERSION),
				NSURLRequestReloadIgnoringLocalCacheData,
				2
			), None, None
		)
		assert response.statusCode() == 200 # found
		version = bytearray(data).decode("utf-8").strip()
	except:
		version = None
	return version


class ApplicationDelegate(NSObject):
	def about_(self, sender):
		app.orderFrontStandardAboutPanelWithOptions_({
			"ApplicationName":    _s(NAME),
			"Version":            _s(VERSION),
			"Copyright":          _s(COPYRIGHT),
			"ApplicationVersion": _s("%s %s" % (NAME, VERSION)),
			"Credits":            _h(CREDITS),
			"ApplicationIcon":    ICON,
		})
	
	def update_(self, sender):
		version = get_version()
		if version is None:
			NSAlert.alertWithError_(
				NSError.errorWithDomain_code_userInfo_("unable to connect to internet,", 1, {})
			).runModal()
			return
		
		if version == VERSION:
			title   = "No update available"
			message = "Your version (%@) of %@ is up to date."
		else:
			title =   "Update available"
			message = "A new version (%@) of %@ is available."
		
		alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
			title,
			"Go to website",
			("Enable" if user_defaults.boolForKey_(NO_NOTIFY) else "Disable") + " notification",
			"Cancel",
			message, version, _s(NAME),
		)
		alert.setIcon_(ICON)
		button = alert.runModal()
		if button == NSAlertDefaultReturn:
			NSWorkspace.sharedWorkspace().openURL_(NSURL.URLWithString_(HOME))
		elif button == NSAlertAlternateReturn:
			user_defaults.setBool_forKey_(not user_defaults.boolForKey_(NO_NOTIFY), NO_NOTIFY)
		else:
			pass
	
	
	def applicationDidFinishLaunching_(self, notification):
		setup_menu(self)
		notify_update()
	
	def applicationWillHide_(self, notification):
		self.fullscreen = toggle_fullscreen(fullscreen=False)
	
	def applicationDidUnhide_(self, notification):
		toggle_fullscreen(fullscreen=self.fullscreen)
	
	def applicationWillTerminate_(self, notification):
		recent_files[url.path()] = current_page
		user_defaults.setObject_forKey_(recent_files, RECENT_FILES)
		presentation_show()
		cleanup_tmp()
	
	def fullScreen_(self, sender):
		toggle_fullscreen(fullscreen=True)


# window utils ##############################################################

def create_window(title, Window=NSWindow, style=NSWindowStyleMaskTitled|NSWindowStyleMaskMiniaturizable, ratio=None):
	if ratio is None:
		frame = PRESENTER_FRAME
	else:
		o, (w, _) = PRESENTER_FRAME
		frame = o, (w, w/ratio)
	window = Window.alloc().initWithContentRect_styleMask_backing_defer_screen_(
		frame,
		style | NSWindowStyleMaskResizable,
		NSBackingStoreBuffered,
		NO,
		None,
	)
	window.setTitle_(title)
	window.makeKeyAndOrderFront_(nil)
	window.setBackgroundColor_(NSColor.blackColor())
	window.setAcceptsMouseMovedEvents_(True)
	return window

def create_view(View, frame=None, window=None):
	if frame is None:
		frame = window.frame()
	view = View.alloc().initWithFrame_(frame)
	view.setBackgroundColor_(NSColor.blackColor())
	if window is not None:
		window.setContentView_(view)
		window.setInitialFirstResponder_(view)
	return view

def add_subview(view, subview, autoresizing_mask=NSViewWidthSizable|NSViewHeightSizable):
	subview.setAutoresizingMask_(autoresizing_mask)
#	subview.setFrameOrigin_((0, 0))
	view.addSubview_(subview)


# presentation window #######################################################

# work around fragile presentation_window.makeFirstResponder_(presenter_view)
class Window(NSWindow):
	def keyDown_(self, event):
		return presenter_window.sendEvent_(event)

presentation_window = create_window(file_name, Window=Window, style=NSWindowStyleMaskBorderless, ratio=ratio)
presentation_window.setMovableByWindowBackground_(True)
presentation_view   = presentation_window.contentView()
frame = presentation_view.frame()

# slides

slide_view = create_view(SlideView, frame=frame)
add_subview(presentation_view, slide_view)

# black view

black_view = create_view(NSView, frame=frame)
add_subview(presentation_view, black_view)

# board view

board_view = create_view(BoardView, frame=frame)
add_subview(presentation_view, board_view)

# web view

web_view = WKWebView.alloc().initWithFrame_configuration_(frame, WKWebViewConfiguration.alloc().init())

class NavigationDelegate(NSObject):
#	def webView_didStartProvisionalNavigation_(self, view, navigation):
	def webView_didFinishNavigation_(self, view, navigation):
		presentation_show(web_view)
navigation_delegate = NavigationDelegate.alloc().init()
web_view.setNavigationDelegate_(navigation_delegate)

add_subview(presentation_view, web_view)

# movie view

movie_view = create_view(MovieView, frame=frame)
add_subview(presentation_view, movie_view)

# video view

_, (w, _) = frame
video_view = VideoView.alloc().initWithFrame_(((w-200-20, 20), (200, 180)))
add_subview(presentation_view, video_view, 0)


# views visibility

def presentation_show(visible_view=slide_view):
	for view in [black_view, board_view, web_view, movie_view]:
		view.setHidden_(view != visible_view)

def toggle_view(view):
	presentation_show(view if view.isHidden() else slide_view)

def toggle_black_view(): toggle_view(black_view)
def toggle_board_view(): toggle_view(board_view)
def toggle_web_view():   toggle_view(web_view)
def toggle_movie_view(): toggle_view(movie_view)
def toggle_video_view():
	if video_view.isHidden():
		video_view.setHidden_(False)
	else:
		video_view.setHidden_(True)

toggle_video_view()
presentation_show()


# presenter window ##########################################################

presenter_window = create_window(file_name)
presenter_view   = create_view(PresenterView, window=presenter_window)

presenter_window.center()
presenter_window.makeFirstResponder_(presenter_view)
presentation_window.makeFirstResponder_(presenter_view)


# handling full screens #####################################################

_switched_screens = False
_content_views = {}

def toggle_fullscreen(fullscreen=None):
	_fullscreen = presenter_view.isInFullScreenMode()
	if fullscreen is None:
		fullscreen = not _fullscreen
	
	if fullscreen != _fullscreen:
		windows = [presentation_window, presenter_window]
		if fullscreen:
			screens = list(window.screen() for window in windows)
			if screens[0] == screens[1]:
				screens = NSScreen.screens()
				screens = (screens[-1], screens[0])
			if _switched_screens:
				screens = reversed(screens)
			for window, screen in zip(windows, screens):
				view = window.contentView()
				view.enterFullScreenMode_withOptions_(screen, {})
				_content_views[window] = view
		else:
			for window in windows:
				_content_views[window].exitFullScreenModeWithOptions_({})
		
		if color_chooser.isVisible():
			color_chooser.orderFront_(None)
		video_view.layout()
		presenter_window.makeFirstResponder_(presenter_view)
	
	return _fullscreen


# main loop #################################################################

application_delegate = ApplicationDelegate.alloc().init()
app.setDelegate_(application_delegate)

# HACK: ensure ApplicationDelegate.applicationDidFinishLaunching_ is called
if restarted:
	NSNotificationCenter.defaultCenter().postNotificationName_object_(
		NSApplicationDidFinishLaunchingNotification, app)

class Refresher(NSObject):
	def refresh_(self, timer=None):
		self.refresh(timer.userInfo())
	
	def refresh(self, views=None):
		if views is None:
			views = [window.contentView() for window in app.windows()]
			views = [view for view in views if view]
		else:
			views = views[:]
		while views:
			view = views.pop()
			view.setNeedsDisplay_(True)
			for subview in view.subviews():
				views.append(subview)
refresher = Refresher.alloc().init()

refresher_timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
	1.,
	refresher, "refresh:",
	[presenter_view], YES)

sys.exit(app.run())
