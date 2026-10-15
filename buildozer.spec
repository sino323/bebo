[app]
title = Mark-LV
package.name = marklv
package.domain = org.marklv
source.dir = .
source.include_exts = py,png,jpg,ttf,json
source.exclude_dirs = config,.git,.github,bin,venv,__pycache__
source.exclude_patterns = desktop.py
version = 1.0.0
requirements = python3,kivy==2.3.0,requests,urllib3,idna,charset-normalizer,certifi,plyer,pyjnius
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 34
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
