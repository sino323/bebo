# Mark-LV

## Desktop (Windows)
    pip install -r requirements.txt
    python desktop.py
First launch asks "Please enter your Gemini API Key" and saves it to `config/api_keys.json`.
Update it later in Settings. The default model (`gemini-2.5-flash`) is editable there too.

## Phone (APK)
Same key prompt on first launch, stored in the app's private storage.
Build the APK one of two ways:
1. Push this folder to GitHub -> Actions -> "Build Mark-LV APK" -> download the `Mark-LV-apk` artifact.
2. On Linux/WSL: `pip install buildozer` then `buildozer android debug` -> APK appears in `bin/`.
Optional: add `assets/NotoEmoji-Regular.ttf` so emojis render on mobile (otherwise they are hidden).
