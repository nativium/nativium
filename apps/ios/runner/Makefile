ROOT_DIR=${PWD}
.DEFAULT_GOAL := help
.PHONY: pods

help:
	@echo "Type: make [rule]. Available options are:"
	@echo ""
	@echo "- help"
	@echo "- clean-derived-data"
	@echo "- pods"
	@echo "- pods-update"
	@echo "- pods-remove"
	@echo "- pods-clear-cache"
	@echo "- format"
	@echo ""

clean-derived-data:
	rm -rf ~/Library/Developer/Xcode/DerivedData

pods:
	rm -rf Pods
	rm -rf Podfile.lock
	rm -rf Runner.xcworkspace
	pod install --no-repo-update

pods-update:
	rm -rf Pods
	rm -rf Podfile.lock
	rm -rf Runner.xcworkspace
	pod install --repo-update

pods-remove:
	rm -rf Pods
	rm -rf Podfile.lock
	rm -rf Runner.xcworkspace

pods-clear-cache:
	pod cache clean 'nativium' --all

format:
	swiftformat --swiftversion 5.0 "Runner/" "Runner-Tv/" "Runner-Watch/" "Runner-WatchExtension/" "Runner-Tests/"
