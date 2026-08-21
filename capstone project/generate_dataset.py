import os
import pandas as pd
import random

def generate_reviews_dataset():
    # Define review templates for positive, neutral, and negative sentiment
    positive_reviews = [
        "The battery life is amazing and the camera quality is excellent. Highly recommend!",
        "Absolutely love this product! It works perfectly and exceeds all my expectations.",
        "Excellent build quality and very comfortable to use daily. Five stars!",
        "Great value for money. Very fast delivery and excellent customer service.",
        "This blender is powerful and easy to clean. Best purchase I've made this year.",
        "The sound quality is outstanding, noise cancellation works like a charm. Very satisfied.",
        "It fits perfectly and the fabric is extremely soft and durable.",
        "Beautiful design and highly functional. It looks great in my living room.",
        "Very fast performance and sleek design. Couldn't ask for a better laptop.",
        "The screen is bright and colors are very vivid. Perfect for watching movies.",
        "Really simple to set up and use. The user manual was clear and helpful.",
        "Outstanding customer service. They resolved my query within minutes.",
        "Super comfortable shoes, perfect for running. Will definitely buy again.",
        "The coffee maker brews quickly and keeps the coffee hot. Love it!",
        "Very robust construction and high-quality materials. Highly durable.",
        "The app integration is seamless and works flawlessly with my smartphone.",
        "Great book! Couldn't put it down. Highly recommend to everyone.",
        "Works exactly as advertised. Clean design and very efficient.",
        "Impressed by the battery life. Lasts more than two days on a single charge.",
        "Very happy with this purchase. It is worth every single penny.",
        "Excellent picture quality and great sound on this TV. Highly recommended.",
        "Quiet and efficient vacuum cleaner. It picks up pet hair easily.",
        "The keyboard has a great tactile feel and the backlighting is lovely.",
        "Stunning quality, the packaging was secure and it arrived early.",
        "Very lightweight and easy to carry around. Ideal for travel."
    ]
    
    neutral_reviews = [
        "It is an okay product, not too good but not bad either. Average quality.",
        "The product works fine, but the setup was a bit confusing.",
        "Decent quality for the price, but don't expect anything extraordinary.",
        "It performs as expected. Nothing special, but it gets the job done.",
        "Average battery life. It lasts about a day which is okay I guess.",
        "The design is nice, but the material feels a bit cheap in hand.",
        "It's a mediocre product. Some features are good, others are lacking.",
        "The packaging was damaged, but the product inside was fine.",
        "It works, but the user interface is a bit dated and slow.",
        "Not bad for the price, but there are better options available.",
        "It is acceptable. Not the best build quality but works for now.",
        "The fit is okay, but the size runs slightly smaller than expected.",
        "It does what it says, but the customer support was hard to reach.",
        "Average sound quality, lack of bass but acceptable for casual listening.",
        "The screen is good, but the battery drains faster than I liked.",
        "Shipping took longer than expected, but the item itself is fine.",
        "It is decent. Nothing to complain about but nothing to praise either.",
        "A standard product. Works well enough for basic everyday tasks.",
        "The fabric is fine, but the color is slightly different from the photos.",
        "The camera is average, does okay in daylight but poor in low light.",
        "Instructions were mediocre, but I managed to set it up eventually.",
        "It's a fair product. Satisfactory performance but not outstanding.",
        "Not a bad purchase, but I am not fully convinced it's worth the price.",
        "Fairly easy to use, though the app crashes occasionally.",
        "It serves its purpose. Neither disappointed nor overly impressed."
    ]
    
    negative_reviews = [
        "Terrible product. It broke on the first day and customer support was useless.",
        "Worst purchase ever. The battery dies in two hours and it gets extremely hot.",
        "Very poor quality. The material is flimsy and feels like it will break easily.",
        "Extremely disappointed. The item looks nothing like the picture.",
        "Waste of money! Do not buy. It stopped working after a week of use.",
        "The product arrived broken and the return process has been a nightmare.",
        "Very slow and laggy. The app crashes every time I try to open it.",
        "Poor customer service. They refused to refund my money for a defective item.",
        "The sound is crackly and the connection keeps dropping. Completely unusable.",
        "It is way too overpriced for such low-quality materials. Highly disappointed.",
        "The size is completely wrong, way too tight and uncomfortable to wear.",
        "Avoid at all costs! The product has a strong chemical smell and is defective.",
        "Cheap plastic construction. It fell once and shattered into pieces.",
        "The software is full of bugs and constant errors. Frustrating experience.",
        "Brews lukewarm coffee and leaks from the bottom. Terrible design.",
        "The vacuum has zero suction power and just pushes dirt around. Useless.",
        "Very noisy and vibrates too much. It is extremely annoying to use.",
        "It keeps freezing and restarting on its own. Absolute garbage.",
        "The package arrived missing half the parts. Had to return it immediately.",
        "Uncomfortable, heavy, and hurts my ears after ten minutes. Do not recommend.",
        "Poorly designed. The buttons are unresponsive and hard to press.",
        "The screen is blurry and has dead pixels. Zero quality control.",
        "Dries out my skin and has an unpleasant smell. Waste of money.",
        "Completely useless. It does not fit the model it claimed to fit.",
        "Very slow delivery and the product died within three days. Frustrated."
    ]

    # Let's generate a list of reviews to build a robust dataset
    data = []
    
    # We want a dataset of 450-500 reviews. Let's create about 160 of each class, slightly varied
    # Add random product names and slight noise to make it feel extremely realistic
    products = [
        "Wireless Headphones", "Smart Watch", "Air Fryer", "Running Shoes", 
        "Ergonomic Office Chair", "Electric Toothbrush", "Bluetooth Speaker", 
        "Espresso Machine", "Robot Vacuum", "Laptop Stand"
    ]
    
    random.seed(42)
    
    for i in range(160):
        # Positive review
        text = random.choice(positive_reviews)
        # Add some random variations or product name prepended
        prod = random.choice(products)
        prefix = random.choice([
            f"I bought this {prod} and ",
            f"My new {prod} arrived and ",
            f"This {prod} is great. ",
            ""
        ])
        full_text = prefix + text[0].lower() + text[1:] if prefix else text
        rating = random.choice([4, 5])
        data.append({"Product": prod, "Review_Text": full_text, "Rating": rating, "Sentiment": "Positive"})
        
    for i in range(160):
        # Neutral review
        text = random.choice(neutral_reviews)
        prod = random.choice(products)
        prefix = random.choice([
            f"Regarding this {prod}, ",
            f"Got this {prod} last week. ",
            f"For a {prod}, ",
            ""
        ])
        full_text = prefix + text[0].lower() + text[1:] if prefix else text
        rating = 3
        data.append({"Product": prod, "Review_Text": full_text, "Rating": rating, "Sentiment": "Neutral"})
        
    for i in range(160):
        # Negative review
        text = random.choice(negative_reviews)
        prod = random.choice(products)
        prefix = random.choice([
            f"Do not buy this {prod}! ",
            f"This {prod} was a complete letdown. ",
            f"Bought this {prod} and regret it. ",
            ""
        ])
        full_text = prefix + text[0].lower() + text[1:] if prefix else text
        rating = random.choice([1, 2])
        data.append({"Product": prod, "Review_Text": full_text, "Rating": rating, "Sentiment": "Negative"})
        
    # Shuffle dataset
    random.shuffle(data)
    
    df = pd.DataFrame(data)
    
    # Ensure directory exists
    os.makedirs("dataset", exist_ok=True)
    df.to_csv("dataset/reviews.csv", index=False)
    print(f"Dataset generated with {len(df)} records at dataset/reviews.csv")

if __name__ == "__main__":
    generate_reviews_dataset()
