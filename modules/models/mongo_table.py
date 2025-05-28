from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex


class TableModel(QAbstractTableModel):
    def __init__(self, headers, data):
        super().__init__()
        self._data = data
        self._headers = headers

    def headerData(self, section, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        if role == Qt.DisplayRole and orientation == Qt.Vertical:
            return section+1

    def data(self, index, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index: QModelIndex = ...):
        return len(self._data)

    def columnCount(self, index: QModelIndex = ...):
        try:
            col = len(self._data[0])
        except Exception:
            col = 1
        return col