import Foundation
import UIKit

struct SimpleOption: Hashable {
    let type: OptionTypeEnum
    let hasSeparator: Bool

    func getDescription() -> String {
        switch type {
        case .appVersion:
            return "OptionAppVersion".localized
        case .multiply:
            return "OptionMultiply".localized
        }
    }

    func getImage() -> UIImage {
        return UIImage(named: "IcoSimpleOption")!.imageWithColor(color: UIColor(hexString: "#F39027")!)!
    }
}
