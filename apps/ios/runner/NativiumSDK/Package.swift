// swift-tools-version:5.5
//
// Local Swift package that consumes the Nativium SDK binary from S3.
//
// This file is refreshed by `make sdk` (it downloads the Package.swift of the
// desired version, already with the correct url + checksum). The values below
// are just a placeholder so the project can be generated/opened offline.

import PackageDescription

let package = Package(
    name: "Nativium",
    platforms: [
        .iOS(.v12),
        .tvOS(.v12),
        .watchOS(.v5),
    ],
    products: [
        .library(name: "nativium", targets: ["nativium"]),
    ],
    targets: [
        .binaryTarget(
            name: "nativium",
            url: "https://nativium.s3.amazonaws.com/dist/ios/1.0.0/dist.zip",
            checksum: "0000000000000000000000000000000000000000000000000000000000000000"
        ),
    ]
)
