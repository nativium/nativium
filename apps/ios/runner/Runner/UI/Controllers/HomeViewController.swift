import UIKit

class HomeViewController: BaseTableViewController {
    var listData: [SimpleOption]?
    let cellIdentifier = "HomeOptionTableViewCell"

    override func createAll() {
        super.createAll()

        // register cell types
        tableView.register(SimpleOptionTableViewCell.self, forCellReuseIdentifier: cellIdentifier)
        tableView.estimatedRowHeight = 50
        tableView.separatorStyle = .none
    }

    override func onLoadNewData() {
        super.onLoadNewData()

        listData = []
        listData?.append(SimpleOption(type: .multiply, hasSeparator: true))
    }

    override func needLoadNewData() -> Bool {
        return true
    }

    override func onTableViewSelectedRow(tableView: UITableView, indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)

        if let option = listData?[indexPath.row] {
            if option.type == .multiply {
                doActionMultiply()
            }
        }
    }

    override func onTableViewCreateCell(tableView: UITableView, indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: cellIdentifier, for: indexPath) as! SimpleOptionTableViewCell

        if let option = listData?[indexPath.row] {
            cell.bind(option: option)
            return cell
        }

        return UITableViewCell()
    }

    override func onTableViewGetNumberOfRows(tableView _: UITableView, section _: Int) -> Int {
        if let listData = listData {
            return listData.count
        }

        return 0
    }

    override func getVCTitle() -> String {
        return "TitleHome".localized
    }

    override func getTitleForAnalytics() -> String {
        return "Home"
    }

    // MARK: Actions

    func doActionMultiply() {
        guard let core = NTVCoreApplicationCore.shared() else { return }

        let message = String(format: "DialogMessageResult".localized, core.multiply(Double.random(in: 1 ... 100), value2: Double.random(in: 1 ... 100)))
        UIHelper.showAlert(parent: self, title: "DialogTitle".localized, message: message, onClose: nil)
    }
}
