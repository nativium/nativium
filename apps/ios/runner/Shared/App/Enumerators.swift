import Foundation

enum NetworkErrorViewAction: Int {
    case refresh = 0
}

enum RemoteDataLoadState: Int {
    case loaded = 0
    case loading = 1
    case notLoaded = 2
}

enum OptionTypeEnum {
    case appVersion
    case multiply
}
