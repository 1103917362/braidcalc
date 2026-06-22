[app]

# (str) Title of your application
title = 公式计算器

# (str) Package name
package.name = braidcalc

# (str) Package domain (needed for android/ios packaging)
package.domain = com.calculator

# (str) Source code where the main.py lives
source.dir = .

# (str) Application versioning
version = 1.0.0

# (list) Requirements
requirements = python3,kivy

# (str) Presplash of the application
presplash.filename = %(source.dir)s/icon.png

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = VIBRATE

# (int) Android API level to use
android.api = 33

# (int) Minimum API level
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use AndroidX support library
android.use_androidx = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 1

# (str) Path to the build directory
build_dir = ./.buildozer