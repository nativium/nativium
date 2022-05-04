import Foundation

enum ActionState: Hashable {
    case inactive
    case loading
    case active

    var isLoading: Bool {
        if case .loading = self {
            return true
        } else {
            return false
        }
    }
}

extension Optional where Wrapped == ActionState {
    var isLoading: Bool {
        return self?.isLoading ?? false
    }
}

enum ViewModelState<TSuccess: Hashable, TError: Hashable>: Hashable {
    case notLoaded
    case loading(data: TSuccess?) // sometimes the page is loading but there is already a valid data, such as refreshing/updating requests that runs after a successful load.
    case loaded(data: TSuccess) // page is fully loaded
    case loadedWithError(data: TSuccess, error: TError) // sometimes the page has valid data loaded, but some error is thrown anyway.
    case failure(error: TError) // page completely failed to load

    var data: TSuccess? {
        switch self {
        case let .loaded(data): return data
        case let .loading(data): return data
        case let .loadedWithError(data, _): return data
        default: return nil
        }
    }

    var error: TError? {
        if case let .failure(error) = self {
            return error
        } else if case let .loadedWithError(_, error) = self {
            return error
        } else {
            return nil
        }
    }

    var isLoading: Bool {
        if case .loading = self {
            return true
        } else {
            return false
        }
    }

    var isNotLoaded: Bool {
        if case .notLoaded = self {
            return true
        } else {
            return false
        }
    }

    static func == (lhs: ViewModelState<TSuccess, TError>, rhs: ViewModelState<TSuccess, TError>) -> Bool {
        switch (lhs, rhs) {
        case (.notLoaded, .notLoaded): return true
        case (.loading(_), .loading(_)): return true
        case (.loaded(_), .loaded(_)): return true
        case (.loadedWithError(_, _), .loadedWithError(_, _)): return true
        case (.failure(_), .failure(_)): return true
        default: return false
        }
    }

    static func === (lhs: ViewModelState<TSuccess, TError>, rhs: ViewModelState<TSuccess, TError>) -> Bool {
        switch (lhs, rhs) {
        case (.notLoaded, .notLoaded): return true
        case let (.loading(lhsData), .loading(rhsData)): return lhsData == rhsData
        case let (.loaded(lhsData), .loaded(rhsData)): return lhsData == rhsData
        case let (.loadedWithError(_, lhsData), .loadedWithError(_, rhsData)): return lhsData == rhsData
        case let (.failure(lhsError), .failure(rhsError)): return lhsError == rhsError
        default: return false
        }
    }
}
