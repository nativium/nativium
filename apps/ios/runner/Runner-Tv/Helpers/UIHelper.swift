import Foundation
import UIKit

class UIHelper {
    static func showAlert(title: String?, message: String?, onClose _: (() -> Void)?) {
        let keyWindow = UIApplication.shared.windows.filter { $0.isKeyWindow }.first

        if var topController = keyWindow?.rootViewController {
            while let presentedViewController = topController.presentedViewController {
                topController = presentedViewController
            }

            let alertController = UIAlertController(title: title, message: message, preferredStyle: .alert)
            alertController.addAction(UIAlertAction(title: "DialogButtonOK".localized, style: .default))
            topController.present(alertController, animated: true, completion: nil)
        }
    }
}
