import UIKit

typealias SWColor = UIColor

public extension SWColor {
    convenience init?(hexString: String) {
        self.init(hexString: hexString, alpha: 1.0)
    }

    convenience init?(hexString: String, alpha: Float) {
        var hex = hexString

        // check for hash and remove the hash
        if hex.hasPrefix("#") {
            hex = String(hex[hex.index(hex.startIndex, offsetBy: 1)...])
        }

        if let _ = hex.range(of: "(^[0-9A-Fa-f]{6}$)|(^[0-9A-Fa-f]{3}$)", options: .regularExpression) {
            // deal with 3 character Hex strings
            if hex.count == 3 {
                let redHex = String(hex[..<hex.index(hex.startIndex, offsetBy: 1)])
                let greenHex = String(hex[hex.index(hex.startIndex, offsetBy: 1) ..< hex.index(hex.startIndex, offsetBy: 2)])
                let blueHex = String(hex[hex.index(hex.startIndex, offsetBy: 2)...])
                hex = redHex + redHex + greenHex + greenHex + blueHex + blueHex
            }

            let redHex = String(hex[..<hex.index(hex.startIndex, offsetBy: 2)])
            let greenHex = String(hex[hex.index(hex.startIndex, offsetBy: 2) ..< hex.index(hex.startIndex, offsetBy: 4)])
            let blueHex = String(hex[hex.index(hex.startIndex, offsetBy: 4) ..< hex.index(hex.startIndex, offsetBy: 6)])

            var redInt: UInt64 = 0
            var greenInt: UInt64 = 0
            var blueInt: UInt64 = 0

            Scanner(string: redHex).scanHexInt64(&redInt)
            Scanner(string: greenHex).scanHexInt64(&greenInt)
            Scanner(string: blueHex).scanHexInt64(&blueInt)

            self.init(red: CGFloat(redInt) / 255.0, green: CGFloat(greenInt) / 255.0, blue: CGFloat(blueInt) / 255.0, alpha: CGFloat(alpha))
        } else {
            self.init()
            return nil
        }
    }

    convenience init?(hex: Int) {
        self.init(hex: hex, alpha: 1.0)
    }

    convenience init?(hex: Int, alpha: Float) {
        let hexString = NSString(format: "%2X", hex)
        self.init(hexString: hexString as String, alpha: alpha)
    }
}
