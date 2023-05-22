# Back-Order-Prediction-Project

In simple terms, a back order is an order that a customer has placed for a product that is currently out of stock, and the supplier is unable to fulfill that order immediately. Instead, the supplier or seller must put the order on hold until they have restocked the product and can fulfill the order at a later date.It happens with premium products which are in high demand like latest products.

Analyzing back order data is important because it can help businesses understand their customers demand patterns and supply chian performance. This analysis tries to minimize the effects by predicting the products which are likely to go on a back order before its occurrence, so that businesses can take necessary actions at an earlier point of time, thus improving overall efficiency.

## Data Description 
The dataset contains 23 columns or features, and their brief descriptions are as follows:

* sku: Unique ID for each product
* national_inv: The current inventory level of the the product
* lead_time: The time taken for the supplier to deliver the product to customer
* in_transit_qty: The number of products that are in transit from the supplier to the seller's warehouse
* forecast_3_month: The forecasted demand for the product in the next 3 months
* forecast_6_month: The forecasted demand for the product in the next 6 months
* forecast_9_month: The forecasted demand for the product in the next 9 months
*sales_1_month: The number of units sold in the last 1 month
* sales_3_month: The number of units sold in the last 3 months
* sales_6_month: The number of units sold in the last 6 months
* sales_9_month: The number of units sold in the last 9 months
* min_bank: The minimum recommended inventory level to be maintained for the product
* potential_issue: A binary feature indicating whether the product has any potential issues that may cause it to go on backorder
* pieces_past_due: The number of units of the product that were ordered but not delivered on time
* perf_6_month_avg: The average performance of the product in the last 6 months
* perf_12_month_avg: The average performance of the product in the last 12 months
* local_bo_qty: The quantity of the product that is currently on backorder at the seller's warehouse
* deck_risk: A binary feature indicating whether the product is at risk of being damaged during transportation or storage
* oe_constraint: A binary feature indicating whether there are any OEM constraints for the product
* ppap_risk: A binary feature indicating whether there is any PPAP (Production Part Approval Process) risk for the product
* stop_auto_buy: A binary feature indicating whether the seller has stopped automatic reordering of the product
* rev_stop: A binary feature indicating whether the seller has stopped revenue recognition for the product
* went_on_backorder: The target variable, which is a binary feature indicating whether the product went on backorder or not

* Home Page 

<p align="center">
  <img src="Image\Screenshot 2023-05-18 183317.png" width='600px'>
</p>

* Predict Page
<p align="center">
  <img src="Image\Screenshot 2023-05-18 183504.png" width='600px' border = "1px">
</p>

## Documents
#### 🌟 Explore the architecture behind this remarkable project and delve into its creation process! 🏗️ Simply follow the links below to delve deeper! 💡✨
* [High-Level Design (HLD)](https://docs.google.com/document/d/1IdOS6Bodc1R1IZ80uP8Rw0eK-CtCnW7E/edit?usp=sharing&ouid=108516397600379304099&rtpof=true&sd=true)
* [Low-Level Design (LLD)](https://docs.google.com/document/d/1-RuXn-oVv-uCk1rssiyt-D4_wp1zh66m/edit?usp=sharing&ouid=108516397600379304099&rtpof=true&sd=true)
* [Architecture](https://docs.google.com/document/d/1M1rrB7N-JI0n_46_4O40CsxLt8Gm0JjX/edit?usp=sharing&ouid=108516397600379304099&rtpof=true&sd=true)
* [Wireframe](https://docs.google.com/document/d/1ZSIHKPxN7o0KNEVwocoNqAVKO2F9oNmT/edit?usp=share_link&ouid=108516397600379304099&rtpof=true&sd=true)
* [Detail-Project-Report (DPR)](https://docs.google.com/document/d/1pYSIQNekmZ_yKuLmtpys-kczNmAJaqEf/edit?usp=sharing&ouid=108516397600379304099&rtpof=true&sd=true)
