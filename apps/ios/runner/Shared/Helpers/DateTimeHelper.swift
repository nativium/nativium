import Foundation

class DateTimeHelper {
    static func getCurrentTimeStamp() -> TimeInterval {
        return Date().timeIntervalSince1970
    }
}
