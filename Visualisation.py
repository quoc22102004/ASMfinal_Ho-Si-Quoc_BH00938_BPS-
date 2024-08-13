import pandas as pd
import matplotlib.pyplot as plt

# Read data from CSV files
khach_hang_df = pd.read_csv('Dữ liệu khách hàng + quốc gia.txt')
marketing_trend_df = pd.read_csv('Dữ liệu market trend.txt')
truy_cap_web_df = pd.read_csv('Dữ liệu truy cập website.txt')
san_pham_va_gia_df = pd.read_csv('Dữ liệu về sản phẩm và giá.txt')
transaction_df = pd.read_csv('transaction.txt')
category_df = pd.read_csv('Category.txt')


# 1 Line Chart: Average of EconomicIndicator by Year and Quarter
marketing_trend_df['Date'] = pd.to_datetime(marketing_trend_df['Date'])
marketing_trend_df['Year'] = marketing_trend_df['Date'].dt.year
marketing_trend_df['Quarter'] = marketing_trend_df['Date'].dt.quarter


# 1. Create a line chart
plt.figure(figsize=(12, 6))
plt.plot(marketing_trend_df['Date'], marketing_trend_df['Value'], marker='o')
plt.title('Average of Value by Year, and Quarter')
plt.xlabel('Date')
plt.ylabel('Average of Value')
plt.grid()
plt.show()








# 2. Customer Distribution by Country
plt.figure(figsize=(10, 6))
customer_country_counts = khach_hang_df['Country'].value_counts()
customer_country_counts.plot(kind='bar', color='skyblue')
plt.title('Customer Distribution by Country')
plt.xlabel('Country')
plt.ylabel('Number of Customers')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('customer_distribution_by_country.png')
plt.show()





# 3. tạo biểu đồ hình tròn
# Kiểm tra các cột trong DataFrame
print("Các cột trong category_df:", category_df.columns)

# Sử dụng đúng DataFrame có cột 'Page'
if 'Page' in category_df.columns:
    page_access_counts = category_df.groupby('Page')['AccessCount'].sum()
else:
    print("Cột 'Page' không tồn tại trong category_df. Hãy kiểm tra lại tệp dữ liệu hoặc sử dụng DataFrame khác.")
    # Nếu cột 'Page' có trong DataFrame khác, sử dụng đúng DataFrame
    page_access_counts = truy_cap_web_df.groupby('Page')['AccessCount'].sum()

# Tạo biểu đồ nếu có dữ liệu hợp lệ
if not page_access_counts.empty:
    plt.figure(figsize=(10, 6))
    page_access_counts.plot(kind='bar', color='lightgreen')
    plt.title('Website Access by Page')
    plt.xlabel('Page')
    plt.ylabel('Access Count')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('website_access_by_page.png')
    plt.show()
else:
    print("Không có dữ liệu hợp lệ để vẽ biểu đồ.")

# 3. Website Access by Page (Pie Chart)
plt.figure(figsize=(8, 8))
page_access_counts = truy_cap_web_df.groupby('Page')['AccessCount'].sum()

# Vẽ biểu đồ hình tròn
plt.pie(page_access_counts, labels=page_access_counts.index, autopct='%1.1f%%', colors=plt.cm.Paired.colors, startangle=90)
plt.title('Website Access by Page')
plt.axis('equal')  # Đảm bảo biểu đồ hình tròn không bị méo
plt.tight_layout()
plt.savefig('website_access_by_page_pie.png')
plt.show()



# 4. Tạo biểu đồ bong bóng với cột 'Price'
# Đọc dữ liệu từ tệp CSV
san_pham_va_gia_df = pd.read_csv('Dữ liệu về sản phẩm và giá.txt')

# Kiểm tra các cột trong DataFrame
print("Các cột trong san_pham_va_gia_df:", san_pham_va_gia_df.columns)

# Tạo biểu đồ bong bóng với cột 'Price'
plt.figure(figsize=(10, 6))

# Sử dụng cột 'Price' cho cả x và y
x = san_pham_va_gia_df['Price']  # Giá sản phẩm
y = san_pham_va_gia_df['Price']  # Giá sản phẩm (hoặc cột khác nếu có)
bubble_size = san_pham_va_gia_df['Price'] * 10  # Kích thước bong bóng dựa trên giá sản phẩm

# Vẽ biểu đồ bong bóng
plt.scatter(x, y, s=bubble_size, alpha=0.5, c='blue', edgecolors='w', linewidth=0.5)

# Thêm tiêu đề và nhãn cho các trục
plt.title('Bubble Chart of Products')
plt.xlabel('Price')
plt.ylabel('Price')

# Thêm nhãn cho mỗi bong bóng
for i in range(len(san_pham_va_gia_df)):
    plt.text(x[i], y[i], san_pham_va_gia_df['ProductName'][i], fontsize=9, ha='center')

# Hiển thị biểu đồ
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('bubble_chart_products.png')
plt.show()




# 5. tạo biểu đò kết hợp
# Đọc dữ liệu từ tệp CSV
transaction_df = pd.read_csv('transaction.txt')

# Loại bỏ khoảng trắng trong tên cột nếu cần
transaction_df.columns = transaction_df.columns.str.strip()

# Kiểm tra lại các cột
print("Các cột trong transaction_df sau khi loại bỏ khoảng trắng:", transaction_df.columns)

# Chuyển đổi cột 'SaleDate' sang định dạng datetime
if 'SaleDate' in transaction_df.columns:
    transaction_df['SaleDate'] = pd.to_datetime(transaction_df['SaleDate'])
else:
    raise KeyError("Cột 'SaleDate' không tồn tại trong transaction_df.")

# Sắp xếp dữ liệu theo ngày
transaction_df = transaction_df.sort_values('SaleDate')

# Tạo biểu đồ kết hợp
fig, ax1 = plt.subplots(figsize=(12, 6))

# Vẽ biểu đồ cột cho doanh thu (Sales)
ax1.bar(transaction_df['SaleDate'], transaction_df['SaleAmount'], color='skyblue', label='Sales')

# Tạo trục y thứ hai để vẽ biểu đồ đường cho số lượng (Quantity)
ax2 = ax1.twinx()
ax2.plot(transaction_df['SaleDate'], transaction_df['Quantity'], color='orange', marker='o', label='Quantity')

# Thêm tiêu đề và nhãn trục
ax1.set_title('Sales and Quantity Over Time')
ax1.set_xlabel('Date')
ax1.set_ylabel('Sales', color='skyblue')
ax2.set_ylabel('Quantity', color='orange')

# Hiển thị chú thích (legend)
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Tự động điều chỉnh bố cục
plt.tight_layout()

# Lưu biểu đồ thành hình ảnh
plt.savefig('sales_quantity_combination_chart.png')

# Hiển thị biểu đồ
plt.show()
