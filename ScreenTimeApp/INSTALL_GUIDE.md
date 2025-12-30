# Installation Guide - Screen Time App

To get this app running on your **Samsung Galaxy A12**, follow these steps:

## 1. Prerequisites
- **Android Studio**: Ensure you have Android Studio installed on your computer.
- **Java 17**: This project uses Java 17 (standard for modern Android).

## 2. Get the Pose Model
The app requires the MediaPipe Pose model to function. 
1. Download `pose_landmarker_lite.task` from [MediaPipe's official site](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker/index#models).
2. Create the assets folder: `app/src/main/assets/`.
3. Copy the `.task` file into that folder.

## 3. Build the App
You can build the app using the command line or Android Studio:

### Via Android Studio (Recommended)
1. Open Android Studio and select **Open**.
2. Navigate to the folder: `/Users/limitless/Documents/AntiGravity/ScreenTimeApp`.
3. Wait for Gradle to sync.
4. Click the **Build** menu > **Build Bundle(s) / APK(s)** > **Build APK(s)**.
5. Once finished, click **locate** in the popup to find `app-debug.apk`.

### Via Terminal
Run this command from the project root:
```bash
./gradlew assembleDebug
```
The APK will be at `app/build/outputs/apk/debug/app-debug.apk`.

## 4. Install on your Galaxy A12
1. **Enable Developer Options**: Go to Settings > About Phone > Software Information > Tap **Build Number** 7 times.
2. **Enable USB Debugging**: Go to Settings > Developer Options > Enable **USB Debugging**.
3. **Connect to PC**: Plug your phone into your computer via USB.
4. **Install**:
   - If you have `adb` installed: 
     ```bash
     adb install app/build/outputs/apk/debug/app-debug.apk
     ```
   - Otherwise: Copy the `.apk` file to your phone's storage and open it using the "My Files" app to install.

## 5. App Setup (On Phone)
1. **Open the App**: Grant **Camera** and **Notification** permissions when prompted.
2. **Disable Battery Optimization**: Follow the popup prompt to "Allow" the app to run in the background.
3. **Enable Accessibility**: 
   - Go to **Settings > Accessibility > Installed Apps**.
   - Find **ScreenTimeApp** and turn it **ON**.
4. **Start Moving!**
