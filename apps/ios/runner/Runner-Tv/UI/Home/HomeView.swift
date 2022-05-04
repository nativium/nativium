
import Foundation
import SwiftUI

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
                            .frame(height: 40)
                            .foregroundColor(Color.clear)
                            .padding(.bottom, 40)
                    ) {
                        if let listData = viewModel.listData.data {
                            ForEach(listData, id: \.self) { item in
                                ZStack {
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
                }
                ZStack(alignment: .top) {
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
