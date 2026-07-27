ROOT_DIR=${PWD}
.DEFAULT_GOAL := help

NATIVIUM_SDK_VERSION = 1.0.0
NATIVIUM_SDK_DIR     = NativiumSDK
NATIVIUM_SDK_URL     = https://nativium.s3.amazonaws.com/dist/ios/$(NATIVIUM_SDK_VERSION)/Package.swift

.PHONY: help project sdk sdk-clean clean-derived-data format

help:
	@echo "Type: make [rule]. Available options are:"
	@echo ""
	@echo "- help"
	@echo "- project            (generate Runner.xcodeproj via XcodeGen)"
	@echo "- sdk                (download the Nativium SDK Package.swift for the version)"
	@echo "- sdk-clean          (clear the SPM cache and re-download the SDK)"
	@echo "- clean-derived-data"
	@echo "- format"
	@echo ""

# generate the Xcode project from project.yml
project:
	xcodegen generate

# download the Package.swift of the version into the local package folder
# (it already comes with the correct url + checksum) and resolve it
sdk:
	mkdir -p $(NATIVIUM_SDK_DIR)
	curl -fsSL "$(NATIVIUM_SDK_URL)" -o $(NATIVIUM_SDK_DIR)/Package.swift
	xcodebuild -resolvePackageDependencies -project Runner.xcodeproj -scheme Runner

# clear the SPM cache and re-resolve (needed only when the SAME version is
# republished, since the url stays the same and the old zip is cached)
sdk-clean:
	rm -rf ~/Library/Caches/org.swift.swiftpm
	rm -rf ~/Library/Developer/Xcode/DerivedData/*/SourcePackages
	$(MAKE) sdk

clean-derived-data:
	rm -rf ~/Library/Developer/Xcode/DerivedData

format:
	swiftformat --swiftversion 5.0 "Runner/" "Runner-Tv/" "Runner-Watch/" "Runner-Tests/" "Shared/"
