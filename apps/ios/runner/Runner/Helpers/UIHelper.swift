import Foundation
import UIKit

class UIHelper {
    static func showAlert(parent: UIViewController, title: String?, message: String?, onClose _: (() -> Void)?) {
        let alertController = UIAlertController(title: title, message: message, preferredStyle: .alert)
        alertController.addAction(UIAlertAction(title: "DialogButtonOK".localized, style: .default))
        parent.present(alertController, animated: true, completion: nil)
    }

    static func isPresentedViewController(viewController: UIViewController?) -> Bool {
        if let viewController = viewController {
            if let _ = viewController.presentingViewController {
                return true
            }

            if viewController.navigationController?.presentingViewController?.presentedViewController == viewController {
                return true
            }

            if viewController.tabBarController?.presentingViewController is UITabBarController {
                return true
            }
        }

        return false
    }
}
