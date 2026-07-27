import Foundation

class HomeViewModel: NSObject, ObservableObject {
    @Published var alertMessage = ""
    @Published var showAlertMessage = false

    @Published var listData: ViewModelState<[SimpleOption], Never> = .notLoaded
    @Published var loadingListData = false

    func loadData() {
        loadingListData = true

        listData = .loading(data: [])

        var data: [SimpleOption] = []
        data.append(SimpleOption(type: .multiply, hasSeparator: true))
        data.append(SimpleOption(type: .appVersion, hasSeparator: false))

        listData = .loaded(data: data)

        loadingListData = false
    }

    func selectItem(_ item: SimpleOption) {
        switch item.type {
        case .multiply:
            doActionMultiply()
        case .appVersion:
            doAppVersion()
        }
    }

    // MARK: Actions

    private func doActionMultiply() {
        guard let core = NTVCoreApplicationCore.shared() else { return }

        let message = String(format: "DialogMessageResult".localized, core.multiply(Double.random(in: 1 ... 100), value2: Double.random(in: 1 ... 100)))
        alertMessage = message
        showAlertMessage = true
    }

    private func doAppVersion() {
        guard let dictionary = Bundle.main.infoDictionary,
              let version = dictionary["CFBundleShortVersionString"] as? String,
              let build = dictionary["CFBundleVersion"] as? String
        else {
            return
        }

        let library = NTVCoreApplicationCore.shared()?.getVersion() ?? ""
        let message = "Library: \(library)\nVersion: \(version)\nBuild: \(build)"

        alertMessage = message
        showAlertMessage = true
    }
}
