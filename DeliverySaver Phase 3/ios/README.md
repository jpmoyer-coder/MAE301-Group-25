# DeliverySaver iOS App

This folder contains a standalone native SwiftUI app. It does not use the Python optimizer or the existing web UI at runtime; it reimplements the delivery comparison logic in Swift and reads `delivery_data.json` from the app bundle.

## Create the Xcode Project

1. Open Xcode.
2. Choose **File > New > Project**.
3. Select **iOS > App**.
4. Use these settings:
   - Product Name: `DeliverySaver`
   - Interface: `SwiftUI`
   - Language: `Swift`
   - Storage: `None`
5. Choose a location for the Xcode project.

## Add the Swift Files

In the Xcode project navigator, add these files from this `ios` folder:

- `Models.swift`
- `ViewModel.swift`
- `ContentView.swift`
- `DeliverySaverApp.swift`

If Xcode generated its own app entry file, either replace its contents with `DeliverySaverApp.swift` or remove the generated `@main` app file from the target. The project should only have one `@main` app type.

## Add the JSON Bundle Data

1. Drag `delivery_data.json` into the Xcode project navigator.
2. In the import dialog, enable **Copy items if needed**.
3. Make sure the app target is checked under **Add to targets**.
4. Confirm the file appears in **Build Phases > Copy Bundle Resources**.

The app loads this resource with:

```swift
Bundle.main.url(forResource: "delivery_data", withExtension: "json")
```

## Running the App

After the Swift files and `delivery_data.json` are added to the Xcode project, run the app from Xcode. The UI appears either in the iOS Simulator window or directly on your iPhone.

### Running in Simulator

1. Open Xcode.
2. Open your existing DeliverySaver Xcode project, or create it using the steps in **Create the Xcode Project** above.
3. Confirm `Models.swift`, `ViewModel.swift`, `ContentView.swift`, `DeliverySaverApp.swift`, and `delivery_data.json` are included in the app target.
4. At the top of Xcode, use the device dropdown next to the app name to select an iPhone simulator, such as **iPhone 15** or **iPhone 16**.
5. Click the Run button (**▶**) or press **Cmd + R**.
6. Wait for Xcode to build and launch the app.
7. The DeliverySaver UI will appear in the iPhone Simulator window. The app opens to the **Compare** tab, where you can select a restaurant, select an item, and view the platform totals.

### Running on a Real iPhone

1. Connect your iPhone to your Mac with a cable.
2. Unlock the iPhone.
3. If the iPhone asks whether to trust the computer, tap **Trust** and enter your passcode.
4. Enable Developer Mode if iOS or Xcode requires it:
   - On the iPhone, open **Settings > Privacy & Security > Developer Mode**.
   - Turn on **Developer Mode**.
   - Restart the iPhone if prompted.
5. In Xcode, open **Xcode > Settings > Accounts**.
6. Click **+**, add your Apple ID, and sign in.
7. Select your project in the Xcode project navigator.
8. Select the app target, then open **Signing & Capabilities**.
9. Check **Automatically manage signing** if it is not already enabled.
10. Choose your Apple ID team from the **Team** dropdown.
11. Make sure the bundle identifier is unique, for example `com.yourname.DeliverySaver`.
12. At the top of Xcode, use the device dropdown next to the app name to select your connected iPhone.
13. Click the Run button (**▶**) or press **Cmd + R**.
14. Xcode will build the app, install it onto the iPhone, and launch it automatically.
15. The DeliverySaver UI will appear on the iPhone screen. Use the **Compare** tab to select a restaurant, select an item, and see the cheapest platform.

## Troubleshooting

1. **No signing certificate**
   - Open **Xcode > Settings > Accounts**.
   - Add your Apple ID.
   - Return to **Signing & Capabilities** and choose your team.

2. **Device not showing in Xcode**
   - Disconnect and reconnect the iPhone cable.
   - Unlock the iPhone.
   - Tap **Trust** if the trust prompt appears.
   - Check the Xcode device dropdown again.

3. **App will not install on iPhone**
   - Enable **Developer Mode** on the iPhone in **Settings > Privacy & Security > Developer Mode**.
   - Restart the iPhone if prompted.
   - Run the app again from Xcode.

4. **Build errors**
   - Open the Xcode console and issue navigator.
   - Confirm all Swift files are included in the app target.
   - Confirm `delivery_data.json` is listed in **Build Phases > Copy Bundle Resources**.
   - Fix the first error shown, then press **Cmd + R** again.

## Files

- `Models.swift`: Codable JSON models and platform definitions.
- `ViewModel.swift`: Data loading, selection state, total calculation, cheapest-platform logic, and savings calculation.
- `ContentView.swift`: SwiftUI tab layout, comparison UI, cards, placeholders, and formatting helpers.
- `DeliverySaverApp.swift`: App entry point.
- `delivery_data.json`: Local restaurant and platform pricing data.