import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import csv


class TaxiManager:
    def __init__(self):
        self.trips = []  # Список поездок [(такси_id, километры, выручка)]

    def load_data_from_file(self, file_path):
    #Загружает данные из CSV файла с контролем ввода
        self.trips = []
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) != 3:
                        raise ValueError("Неправильный формат данных в файле.")
                    taxi_id = row[0].strip()
                    distance = int(row[1].strip())
                    revenue = float(row[2].strip())
                    self.trips.append((taxi_id, distance, revenue))
            messagebox.showinfo("Успех", "Данные загружены успешно!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке данных: {e}")

    def segment_trips_by_distance(self):
    #Сегментирует поездки по продолжительности (дискретнопо 10 км)
        segments = {}
        for _, distance, _ in self.trips:
            key = f"{(distance // 10) * 10}-{(distance // 10 + 1) * 10}км"
            segments[key] = segments.get(key, 0) + 1
        return segments

    def segment_taxi_by_revenue(self):
    #Сегментирует такси по выручке
        revenue_segments = {}
        for taxi_id, _, revenue in self.trips:
            if taxi_id not in revenue_segments:
                revenue_segments[taxi_id] = 0
                revenue_segments[taxi_id] += revenue
        return revenue_segments

    def visualize_pie_chart(self, data, title):
    #Визуализирует данные в виде круговой диаграммы
        labels = data.keys()
        sizes = data.values()
        plt.figure(figsize=(8, 6))
        explode = [0.1, 0.1, 0.1, 0.1]
        plt.pie(sizes, labels=labels, explode=explode, shadow=True, autopct='%1.1f%%', startangle=140)
        plt.title(title)
        plt.show()

    def visualize_bar_chart(self, data, title, xlabel, ylabel):
    #Визуализирует данные в виде столбиковой диаграммы
        labels = list(data.keys())
        values = list(data.values())
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color='skyblue')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.xticks(rotation=45)
        plt.show()


class TaxiApp:
    def __init__(self, root):
        self.manager = TaxiManager()
        self.root = root
        self.root.title("Система управления такси")

        # Создаем элементы интерфейса
        self.label = tk.Label(root, text="Загрузите данные о поездках такси")
        self.label.pack(pady=10)

        self.load_button = tk.Button(root, text="Загрузить файл", command=self.load_file)
        self.load_button.pack(pady=5)

        self.segment_distance_button = tk.Button(root, text="Сегментация по расстоянию",
        command=self.segment_by_distance)
        self.segment_distance_button.pack(pady=5)

        self.segment_revenue_button = tk.Button(root, text="Сегментация по выручке", command=self.segment_by_revenue)
        self.segment_revenue_button.pack(pady=5)

        # Центрирование окна по середине
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 400
        window_height = 300

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def load_file(self):
    #Загрузка данных из файла
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.manager.load_data_from_file(file_path)

    def segment_by_distance(self):
    #Сегментация поездок по расстоянию и визуализация
        segments = self.manager.segment_trips_by_distance()
        if segments:
            self.manager.visualize_pie_chart(segments, "Сегментация поездок по продолжительности (км)")
        else:
            messagebox.showwarning("Предупреждение", "Данные о поездках отсутствуют!")

    def segment_by_revenue(self):
    #Сегментация такси по выручке и визуализация
        revenue_segments = self.manager.segment_taxi_by_revenue()
        if revenue_segments:
            self.manager.visualize_bar_chart(revenue_segments, "Сегментация такси по выручке", "ID такси", "Выручка")
        else:
            messagebox.showwarning("Предупреждение", "Данные о выручке отсутствуют!")



if __name__ == "__main__":
    root = tk.Tk()
    
     screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 300
    window_height = 200

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    app = TaxiApp(root)
    print(f"Время работы программы: {final_time:.2f} секунд")
    root.mainloop()
