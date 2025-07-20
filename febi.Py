import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt

class KNearestNeighbors:
    def __init__(self, k=3):
        self.k = k
        
    def euclidean_distance(self, x1, x2):
        """
        Menghitung jarak euclidean antara dua titik
        """
        return np.sqrt(np.sum((x1 - x2)**2))
    
    def fit(self, X, y):
        """
        Menyimpan data training
        """
        self.X_train = X
        self.y_train = y
    
    def predict(self, X):
        """
        Memprediksi label untuk setiap sampel dalam X
        """
        y_pred = [self._predict(x) for x in X]
        return np.array(y_pred)
    
    def _predict(self, x):
        """
        Memprediksi label untuk satu sampel
        """
        # Hitung jarak ke semua titik training
        distances = [self.euclidean_distance(x, x_train) for x_train in self.X_train]
        
        # Urutkan berdasarkan jarak
        k_indices = np.argsort(distances)[:self.k]
        
        # Ambil label dari k tetangga terdekat
        k_nearest_labels = [self.y_train[i] for i in k_indices]
        
        # Pilih label yang paling umum
        most_common = max(set(k_nearest_labels), key=k_nearest_labels.count)
        
        return most_common

def main():
    # Contoh dataset (Iris)
    from sklearn.datasets import load_iris
    
    # Load dataset
    iris = load_iris()
    X = iris.data
    y = iris.target
    
    # Bagi dataset menjadi training dan testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Normalisasi fitur
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Inisialisasi dan latih KNN
    knn = KNearestNeighbors(k=3)
    knn.fit(X_train_scaled, y_train)
    
    # Prediksi
    y_pred = knn.predict(X_test_scaled)
    
    # Evaluasi model
    accuracy = accuracy_score(y_test, y_pred)
    print("Akurasi:", accuracy)
    
    # Laporan klasifikasi
    print("\nLaporan Klasifikasi:")
    print(classification_report(y_test, y_pred, target_names=iris.target_names))
    
    # Visualisasi
    plt.figure(figsize=(10, 6))
    plt.scatter(X_test_scaled[y_pred == y_test, 0], 
                X_test_scaled[y_pred == y_test, 1], 
                c='green', label='Benar')
    plt.scatter(X_test_scaled[y_pred != y_test, 0], 
                X_test_scaled[y_pred != y_test, 1], 
                c='red', label='Salah')
    plt.title('Hasil Prediksi KNN')
    plt.xlabel('Fitur 1 (Dinormalisasi)')
    plt.ylabel('Fitur 2 (Dinormalisasi)')
    plt.legend()
    plt.show()

# Contoh penggunaan tambahan
def cross_validation_example():
    from sklearn.model_selection import cross_val_score
    from sklearn.datasets import load_iris
    
    # Load dataset
    iris = load_iris()
    X = iris.data
    y = iris.target
    
    # Uji coba berbagai nilai k
    k_values = range(1, 21)
    cv_scores = []
    
    for k in k_values:
        knn = KNearestNeighbors(k=k)
        scores = cross_val_score(knn, X, y, cv=5)
        cv_scores.append(scores.mean())
    
    # Plot hasil cross validation
    plt.figure(figsize=(10, 6))
    plt.plot(k_values, cv_scores, marker='o')
    plt.title('Pengaruh Nilai K terhadap Akurasi')
    plt.xlabel('Jumlah Tetangga (K)')
    plt.ylabel('Akurasi Cross Validation')
    plt.show()

if __name__ == "__main__":
    main()
    # cross_validation_example()