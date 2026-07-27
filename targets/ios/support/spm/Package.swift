// swift-tools-version:5.5
import PackageDescription

let package = Package(
    name: "{PRODUCT_NAME}",
    platforms: [
        .iOS(.v12),
        .tvOS(.v12),
        .watchOS(.v5),
    ],
    products: [
        .library(
            name: "{PROJECT_NAME}",
            targets: ["{PROJECT_NAME}"]
        ),
    ],
    targets: [
        .binaryTarget(
            name: "{PROJECT_NAME}",
            url: "{SPM_URL}",
            checksum: "{SPM_CHECKSUM}"
        ),
    ]
)
