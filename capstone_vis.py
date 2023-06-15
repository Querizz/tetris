import streamlit as st
import pandas as pd
import altair as alt
import humanize

st.set_page_config(
    page_title="dashboard",
    layout="wide"
)

df_customer_analysis = pd.read_csv('customer_analysis.csv')
df_geo_analysis = pd.read_csv('geolocation_analysis.csv')
df_order_items_analysis = pd.read_csv('order_items_analysis.csv')
df_seller_analysis = pd.read_csv('seller_analysis.csv')

#df_customer_analysis = pd.read_csv(r'D:\file imam\_Data Analyst\tetris\Capstone Project\DataSet\brazillian ecommerce dataset\csv_file\customer_analysis.csv')
#df_geo_analysis = pd.read_csv(r'D:\file imam\_Data Analyst\tetris\Capstone Project\DataSet\brazillian ecommerce dataset\csv_file\geolocation_analysis.csv')
#df_order_items_analysis = pd.read_csv(r'D:\file imam\_Data Analyst\tetris\Capstone Project\DataSet\brazillian ecommerce dataset\csv_file\order_items_analysis.csv')
#df_seller_analysis = pd.read_csv(r'D:\file imam\_Data Analyst\tetris\Capstone Project\DataSet\brazillian ecommerce dataset\csv_file\seller_analysis.csv')


st.title('Dashboard Olist E-Commerce')
st.header('Latar Belakang')
st.write('Olist adalah sebuah platform e-commerce yang berbasis di Brazil. Platform ini menyediakan layanan untuk para penjual dan pembeli dalam menjual dan membeli berbagai produk secara online. Olist menyediakan infrastruktur yang memungkinkan penjual untuk memasarkan dan mengelola produk mereka dengan lebih efisien, sementara pembeli dapat menemukan beragam pilihan produk dari berbagai penjual yang terdaftar di platform. Olist juga memberikan dukungan dalam hal logistik, pembayaran, dan layanan pelanggan untuk memastikan pengalaman jual beli yang baik bagi semua pihak yang terlibat. Dengan demikian, Olist berperan sebagai perantara antara penjual dan pembeli dalam ekosistem e-commerce di Brazil')
st.write('Data yang terkumpul dari platform ini mencakup berbagai informasi penting seperti transaksi penjualan, profil pelanggan, produk yang dijual, dan lainnya. Melalui analisis data Olist e-commerce, kita dapat menggali wawasan yang berharga untuk mendapatkan pemahaman lebih baik tentang perilaku pembeli, tren pasar, serta performa penjual.')
st.header('Sumber Data')
st.subheader('Olist')
st.write('Projek ini dilakukan menggunakan Open Data yang dipublikasikan langsung oleh pihak Olist melalui www.kaggle.com')
#ubah dtype ke datetime
df_customer_analysis['order_purchase_timestamp'] = pd.to_datetime(df_customer_analysis['order_purchase_timestamp'])
df_order_items_analysis['order_purchase_timestamp'] = pd.to_datetime(df_order_items_analysis['order_purchase_timestamp'])
# feature engineering
df_customer_analysis['date'] = df_customer_analysis['order_purchase_timestamp'].dt.date
df_order_items_analysis['date'] = df_order_items_analysis['order_purchase_timestamp'].dt.date

with st.sidebar:
    st.subheader("Olist E-Commerce Dashboard")
    st.write("by Imam Qalbun Salim")
    analisis = st.selectbox(
        "Welcome",
        ("Customer Analysis","Product Analysis")
    )
if analisis == "Customer Analysis":
    st.title('Data Preview')
    st.dataframe(df_customer_analysis.head())
    st.title("Customer Analysis")
    sales_line_tahun = st.selectbox(
        "pilih tahun",
        (2017,2018)
    )
    col1, col2 = st.columns([1,3])
    with col1: 
        st.metric(
            label = 'Peak Sales',
            value = df_customer_analysis[df_customer_analysis['order_purchase_timestamp'].dt.year == sales_line_tahun].groupby('date')['order_id'].count().max()
        )
    with col2:
        st.metric(
            label = 'Total Omzet of '+ str(sales_line_tahun),
            value = humanize.intword(df_customer_analysis[df_customer_analysis['order_purchase_timestamp'].dt.year == sales_line_tahun].groupby('date')['price_idr'].sum().max()) + ' IDR'
        )
    if sales_line_tahun == 2017:
        st.header("Understanding the Seasonal Effect in"+' '+str(sales_line_tahun))
    elif sales_line_tahun == 2018:
        st.header("Understanding the Sales Trend in"+' '+str(sales_line_tahun))
    sales_line = alt.Chart(df_customer_analysis[df_customer_analysis['order_purchase_timestamp'].dt.year == sales_line_tahun]).mark_line().encode(
        alt.X('date', title ='tanggal'),
        alt.Y('order_id', title='total sales', aggregate='count')
    )
    st.altair_chart(sales_line, use_container_width=True)
    if sales_line_tahun == 2017:
        st.subheader("November - December Sales Surge")
        st.write("Grafik garis di atas menggambarkan data penjualan total (jumlah) dari Olist E-Commerce seiring waktu. Salah satu pengamatan yang mencolok adalah lonjakan signifikan dalam penjualan selama bulan November - Desember. Musim liburan, yang meliputi Natal, Hanukkah, dan Tahun Baru, memainkan peran penting dalam mendorong pengeluaran konsumen. Selama bulan November - Desember, orang cenderung membeli hadiah, dekorasi, dan barang lainnya, yang mengakibatkan peningkatan penjualan bagi bisnis di berbagai industri.")
        st.write("Dalam mengoptimalkan penjualan selama musim liburan, perusahaan dapat mengambil langkah-langkah berikut:")
        st.write("1. Promosi: Rencanakan kampanye promosi menarik dengan diskon, penawaran bundle, hadiah gratis, atau pengiriman gratis.")
        st.write("2. Stok: Persiapkan stok yang cukup berdasarkan proyeksi permintaan dan tren pasar untuk menghindari kekurangan.")
        st.write("3. Pemasaran: Tingkatkan upaya pemasaran melalui saluran online, media sosial, iklan cetak, atau promosi email untuk meningkatkan visibilitas merek dan mencapai pelanggan potensial.")
    elif sales_line_tahun == 2018:
        st.subheader("May and September Decline")
        st.write("Grafik menunjukkan penjualan total Olist E-Commerce seiring waktu. Tampak penurunan signifikan pada Mei (pertengahan hingga akhir) 2018. Ini disebabkan oleh efek musiman dan mogok truk di Brasil yang berlangsung selama 11 hari. Peristiwa tersebut mengganggu pasokan, transportasi, dan menyebabkan kelangkaan produk, mempengaruhi kebiasaan belanja konsumen. Pemahaman terhadap peristiwa eksternal dan pengaruhnya pada pola penjualan penting bagi bisnis dalam mengoptimalkan strategi pemasaran dan manajemen persediaan selama periode yang sulit.")
        st.write("Sumber: [The New York Times](https://www.nytimes.com/2018/05/28/world/americas/brazil-truckers-strike-economy.html)")    
        st.write("Sementara itu, pada September 2018, terjadi peristiwa penting yang berpotensi menjadi penyebab penurunan penjualan. Pada tanggal 2 September, Museum Nasional Brasil terbakar dan mengalami kerusakan parah. Kondisi ini mungkin mempengaruhi suasana dan minat konsumen untuk berbelanja online, termasuk di Olist E-Commerce. Memahami peristiwa eksternal seperti ini membantu perusahaan merespons dengan tepat terhadap faktor-faktor yang dapat memengaruhi pola penjualan.")    
        st.write("Sumber: [National Geographic](https://www.nationalgeographic.com/science/article/news-museu-nacional-fire-rio-de-janeiro-natural-history)")
    total_city_count = df_customer_analysis[df_customer_analysis['order_purchase_timestamp'].dt.year == sales_line_tahun]['customer_city'].value_counts().to_frame().reset_index()['count'].sum()
    top_city = df_customer_analysis[df_customer_analysis['order_purchase_timestamp'].dt.year == sales_line_tahun]['customer_city'].value_counts().head(20).to_frame().reset_index()
    st.header("Exploring Customer Distribution in"+' '+str(sales_line_tahun))
    col4, col5, coly = st.columns(3)
    with col4: 
        st.metric(
            label = 'City with Most Customers in '+str(sales_line_tahun),
            value = top_city['customer_city'][0]
        )
    with col5:
        st.metric(
            label = 'Number of Customers from '+ str(top_city['customer_city'][0]),
            value = top_city['count'][0]
        )
    with coly:
        st.metric(
            label = 'Top 3 City Account for Total Customer',
            value = '{:.2f}'.format((top_city['count'].head(3).sum()/total_city_count)*100) + '%'
        )
    bar_chart = alt.Chart(top_city).mark_bar().encode(
        alt.X('customer_city', title ='Customer\'s City', sort='-y'),
        alt.Y('count',title ='count'),
        color=alt.condition(
            alt.datum.rank < 4,
            alt.value('seagreen'),
            alt.value('crimson')
        )
    ).transform_window(
        rank='rank(count)',
        sort=[alt.SortField('count', order='descending')]
    )
    st.altair_chart(bar_chart, use_container_width=True)
    st.subheader("Optimizing Marketing Strategies")
    st.write("Salah satu temuan utama dalam analisis ini adalah bahwa tiga kota teratas (São Paulo, Rio de Janeiro, dan Belo Horizonte) pada tahun 2017 berkontribusi hampir 25% dari total jumlah pelanggan. Hal ini menunjukkan bahwa fokus pada kota-kota ini dapat memberikan manfaat besar dalam upaya pemasaran dan pertumbuhan bisnis")
    st.write("Selain itu, temuan ini juga menyoroti potensi peluang untuk melakukan penetrasi pasar di kota-kota dengan jumlah pelanggan yang sedikit. Dengan mengidentifikasi kota-kota ini sebagai wilayah yang belum tergarap sepenuhnya, perusahaan dapat mengambil langkah-langkah strategis untuk memperluas jangkauan dan meningkatkan pangsa pasar di area yang belum terpenuhi potensinya.")
    col6, col7 = st.columns(2)
    #-------
    with col6:
        st.header('Payment Method Preferences in'+' '+str(sales_line_tahun))
        top_payment = df_customer_analysis[df_customer_analysis['order_purchase_timestamp'].dt.year == sales_line_tahun]['payment_type'].value_counts().to_frame().reset_index()
        payment_bar_chart = alt.Chart(top_payment).mark_bar().encode(
            alt.X('payment_type', title ='Payment Type', sort='-y'),
            alt.Y('count',title ='count')
        )
        st.altair_chart(payment_bar_chart, use_container_width=True)
    with col7:
        st.header("Payment Preferences Across Cities")
        payment = st.selectbox(
            "Pilih Payment Types",
            ('credit_card','boleto','voucher','debit_card')
        )
        top_payment_city = df_customer_analysis[(df_customer_analysis['order_purchase_timestamp'].dt.year == sales_line_tahun) & (df_customer_analysis['payment_type'] == payment)]['customer_city'].value_counts().head(10).to_frame().reset_index()
        top_payment_city_chart = alt.Chart(top_payment_city).mark_bar().encode(
            alt.X('customer_city', title ='Customer\'s City', sort='-y'),
            alt.Y('count',title ='count')
        )
        st.altair_chart(top_payment_city_chart, use_container_width=True)
    st.write("**Dominasi Kartu Kredit:** Kartu kredit menjadi pilihan utama untuk pembayaran, menekankan kenyamanan dan fleksibilitasnya.")
    st.write("**Keberartian Boleto:** Boleto tetap populer, mungkin karena transaksi berbasis tunai dan penerimaan yang luas.")
    st.write("**Voucher yang Menarik:** Pelanggan tertarik dengan voucher berkat diskon, promosi, dan penawaran khusus.")
    st.write("**Preferensi yang Lebih Rendah untuk Kartu Debit**: Kartu debit mendapatkan peringkat lebih rendah, mungkin karena keterbatasan ketersediaan atau daya tarik manfaat kartu kredit.")
    #-----



elif analisis == "Product Analysis":
    st.title("Data Preview")
    st.dataframe(df_customer_analysis.head())
    st.title("Product Analysis")
    pilih_tahun = st.selectbox(
        "pilih tahun",
        (2017,2018)
    )
    st.header("Bestselling Products of"+' '+str(pilih_tahun))
    top_product_data = df_order_items_analysis[df_order_items_analysis['order_purchase_timestamp'].dt.year == pilih_tahun]['product_category_name_english'].value_counts().to_frame().reset_index()
    col8, col9, colx = st.columns(3)
    with col8: 
        st.metric(
            label = 'Best Selling Product in '+str(pilih_tahun),
            value = top_product_data['product_category_name_english'][0]
        )
    with col9:
        st.metric(
            label = 'Sold a Total of',
            value = top_product_data['count'][0]
        )
    with colx:
        st.metric(
            label ='Top 10 Products Account For the Total Sales',
            value = '{:.2f}'.format((top_product_data['count'].head(10).sum()/top_product_data['count'].sum())*100) + '%'
        )
    product_bar = alt.Chart(top_product_data).mark_bar().encode(
        alt.X('product_category_name_english', title='Product Name',sort='-y'),
        alt.Y('count', title='# Sold'),
        color=alt.condition(
            alt.datum.rank < 11,
            alt.value('seagreen'),
            alt.value('crimson')
        )
    ).transform_window(
        rank='rank(count)',
        sort=[alt.SortField('count', order='descending')]
    )
    st.altair_chart(product_bar, use_container_width=True)
    st.subheader("Wide Product Selection, Good or Bad?")
    st.write("10 besar produk terlaris dari total 72 mencapai sekitar 65% dari total penjualan. Konsentrasi ini menyoroti dampak signifikan yang dapat ditimbulkan oleh beberapa produk tertentu terhadap perolehan pendapatan secara keseluruhan. Dengan berfokus pada produk berkinerja tinggi ini, bisnis dapat mengalokasikan sumber dayanya secara efektif dan memaksimalkan profitabilitasnya.")
    st.write("Namun, sangat penting untuk mencapai keseimbangan dalam hal pemilihan produk. Memiliki jumlah produk yang berlebihan dapat membuat pelanggan bingung dan berpotensi melemahkan penjualan. Seperti yang terjadi di sini, bahwa 62 dari 72 produk hanya dapat menyumbang sekitar 35% dari total penjualan. Penting untuk merampingkan penawaran produk dan memprioritaskan yang berkinerja terbaik untuk menghindari kebingungan dan memastikan pengalaman pelanggan yang lancar.")

    col10, col11 = st.columns(2)
    with col10: 
        top_city = df_customer_analysis[df_customer_analysis['order_purchase_timestamp'].dt.year == pilih_tahun]['customer_city'].value_counts().head(10).to_frame().reset_index()
        st.header("Bestselling Products of"+' '+str(pilih_tahun)+' '+'for Top 10 City')
        pilih_kota = st.selectbox(
            "pilih kota",
            (top_city['customer_city'][0],top_city['customer_city'][1],top_city['customer_city'][2],top_city['customer_city'][3],top_city['customer_city'][4],top_city['customer_city'][5],top_city['customer_city'][6],top_city['customer_city'][7],top_city['customer_city'][8],top_city['customer_city'][9])
        )
        product_bar_city_data = df_customer_analysis[(df_customer_analysis['order_purchase_timestamp'].dt.year == pilih_tahun) & (df_customer_analysis['customer_city'] == pilih_kota)]['product_category_name_english'].value_counts().head(10).to_frame().reset_index()
        product_bar_city = alt.Chart(product_bar_city_data).mark_bar().encode(
            alt.X('product_category_name_english', title='Product Name',sort='-y'),
            alt.Y('count', title='# Sold')
        )
        st.altair_chart(product_bar_city, use_container_width=True)
    with col11:
        st.header("Bestselling Products of"+' '+str(pilih_tahun)+' '+'for each Payment Method')
        pilih_payment = st.selectbox(
            "pilih payment",
            ('credit_card','boleto','voucher','debit_card')
        )
        product_bar_payment_data = df_customer_analysis[(df_customer_analysis['order_purchase_timestamp'].dt.year == pilih_tahun) & (df_customer_analysis['payment_type'] == pilih_payment)]['product_category_name_english'].value_counts().head(10).to_frame().reset_index()
        product_bar_payment = alt.Chart(product_bar_payment_data).mark_bar().encode(
            alt.X('product_category_name_english', title='Product Name',sort='-y'),
            alt.Y('count', title='# Sold')
        )
        st.altair_chart(product_bar_payment, use_container_width=True)
    st.subheader("Regional Preferences and Payment Method Insights")
    st.write("Analisis terhadap 10 kota teratas mengungkapkan pola menarik mengenai produk terlaris. Di antara kota-kota tersebut, Bed Bath Table menjadi produk terlaris di 6 dari 10 kota, menunjukkan popularitas dan permintaan yang luas. Produk Health & Beauty menduduki posisi teratas di 3 kota, menyoroti pentingnya perawatan pribadi dan kesehatan bagi konsumen. Selain itu, Furniture Decor menjadi produk terlaris di 2 kota, menekankan pentingnya tren dekorasi rumah dan perabotan. Memahami preferensi regional ini dapat membimbing strategi pemasaran dan pengelolaan inventaris untuk memenuhi kebutuhan dan preferensi khusus setiap kota.")
    st.write("Dalam tiga metode pembayaran, yaitu kartu kredit, boleto, dan voucher, terdapat satu kesamaan bahwa 'Bed Bath Table' menjadi produk terlaris. Namun, menariknya, ketika melihat pembayaran dengan kartu debit, terdapat perbedaan yang menonjol. Produk terlaris dalam kategori kartu debit adalah 'Sport Leisure', sementara 'Bed Bath Table' justru berada di posisi ke-5. Hal ini mengindikasikan preferensi konsumen yang berbeda tergantung pada metode pembayaran yang digunakan. Meskipun 'Bed Bath Table' sangat populer dalam beberapa metode pembayaran, tetapi tidak demikian ketika menggunakan kartu debit. Informasi ini penting bagi perusahaan untuk memahami kebutuhan dan preferensi pelanggan berdasarkan metode pembayaran yang mereka pilih, sehingga dapat mengoptimalkan strategi pemasaran dan penawaran produk yang sesuai dengan segmen pembeli yang berbeda.")
    st.header('Number of Products Sold Each Month')
    pilih_produk = st.selectbox(
        "pilih produk",
        (top_product_data['product_category_name_english'][0],top_product_data['product_category_name_english'][1],top_product_data['product_category_name_english'][2],top_product_data['product_category_name_english'][3],top_product_data['product_category_name_english'][4],top_product_data['product_category_name_english'][5],top_product_data['product_category_name_english'][6],top_product_data['product_category_name_english'][7],top_product_data['product_category_name_english'][8],top_product_data['product_category_name_english'][9])
    )
    df_monthly_sales = df_customer_analysis[(df_customer_analysis['order_purchase_timestamp'].dt.year == pilih_tahun) & (df_customer_analysis['product_category_name_english'] == pilih_produk)].groupby(df_customer_analysis['order_purchase_timestamp'].dt.month)['product_category_name_english'].count().to_frame().reset_index()
    monthly_bar_sales = alt.Chart(df_monthly_sales).mark_bar().encode(
        alt.X('order_purchase_timestamp', title='Bulan Ke-',scale=alt.Scale(domain=[1,12]),axis=alt.Axis(tickCount=12, labelExpr="datum.value % 1 ? '' : datum.label")),
        alt.Y('product_category_name_english', title='Count')
    )
    st.altair_chart(monthly_bar_sales, use_container_width=True)
    
    








elif analisis == "pilihan3":
    st.title("wait")