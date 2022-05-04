
import Foundation
import SwiftUI
import WatchKit

struct HomeView: View {
    @ObservedObject private(set) var viewModel = HomeViewModel()

    private let mainColor = UIColor(hexString: "#F39027")!
    private let rowBackgroundColor = UIColor(hexString: "#332F2E")!

    var body: some View {
        ZStack {
            ZStack(alignment: .top) {
                List {
                    Section(
                        header: Rectangle()
                            .frame(height: 26)
                            .foregroundColor(Color.clear)
                    ) {
                        if let listData = viewModel.listData.data {
                            ForEach(listData, id: \.self) { item in
                                Button {
                                    viewModel.selectItem(item)
                                } label: {
                                    HStack {
                                        Image(uiImage: item.getImage())
                                        Text("\(item.getDescription())")
                                            .foregroundColor(Color(mainColor))
                                    }
                                }
                                .listRowBackground(
                                    RoundedRectangle(cornerRadius: 8)
                                        .foregroundColor(Color(rowBackgroundColor))
                                )
                            }
                        }
                    }
                }
                ZStack(alignment: .top) {
                    LinearGradient(gradient: Gradient(colors: [Color.black, Color.black, Color.black, Color.clear]), startPoint: .top, endPoint: .bottom)
                    Text("Home")
                        .font(.headline)
                        .foregroundColor(Color(hex: "#F39027"))
                }
                .frame(height: 30)
            }

            LoadingView().isHidden(!viewModel.loadingListData)
        }
        .alert(isPresented: $viewModel.showAlertMessage) {
            Alert(title: Text("DialogTitle".localized), message: Text(viewModel.alertMessage), dismissButton: Alert.Button.cancel(Text("DialogButtonOK".localized)))
        }
        .onAppear {
            DispatchQueue.main.async {
                self.viewModel.loadData()
            }
        }
    }
}

class HomeHostingController: WKHostingController<HomeView> {
    override var body: HomeView {
        return HomeView()
    }
}
