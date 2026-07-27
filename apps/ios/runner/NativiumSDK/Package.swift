// swift-tools-version:5.5
import PackageDescription

let package = Package(
    name: "Nativium",
    platforms: [
        .iOS(.v12),
        .tvOS(.v12),
        .watchOS(.v5),
    ],
    products: [
        .library(
            name: "nativium",
            targets: ["nativium"]
        ),
    ],
    targets: [
        .binaryTarget(
            name: "nativium",
            url: "https://nativium.s3.amazonaws.com/dist/ios/1.0.0/dist.zip",
            checksum: "9bc44e837c0a7f4540f6145a6783c2379a10055cd5976ae04dfed698db74cf91"
        ),
    ]
)
