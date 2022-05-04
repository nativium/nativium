import XCTest

class CoreTests: XCTestCase {
    override func setUpWithError() throws {
        // Put setup code here. This method is called before the invocation of each test method in the class.
    }

    override func tearDownWithError() throws {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
    }

    func testVersion() throws {
        let version = NTVCoreApplicationCore.shared()?.getVersion() ?? ""
        let versionName = version.split { $0 == " " }[0]
        assert(versionName == "1.0.0")
    }

    func testMultiply() throws {
        let result = NTVCoreApplicationCore.shared()?.multiply(3.0, value2: 4.0)
        assert(result == 12.0)
    }

    func testPerformanceExample() throws {
        // This is an example of a performance test case.
        measure {
            // Put the code you want to measure the time of here.
        }
    }
}
