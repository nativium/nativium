import SwiftUI

@main
struct RunnerWatchApp: App {
    @WKApplicationDelegateAdaptor(ExtensionDelegate.self) var delegate

    var body: some Scene {
        WindowGroup {
            HomeView()
        }
    }
}
