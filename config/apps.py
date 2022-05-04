# -----------------------------------------------------------------------------
def run(proj_path, params):
    return {
        "ios": {
            "runner": {
                "name": "Runner",
                "bundle-id": "com.nativium.app",
                "scheme": "Runner",
                "workspace": "Runner.xcworkspace",
                "product": "Runner.app",
                "destination": {
                    "build": "generic/platform=iOS",
                    "test": "platform=iOS Simulator,name=iPhone 13",
                    "archive": "generic/platform=iOS",
                },
            },
        },
        "android": {
            "runner": {
                "name": "Runner",
                "package": "com.nativium.app",
                "activity": "com.nativium.app.ui.activity.MainActivity",
            },
        },
    }
