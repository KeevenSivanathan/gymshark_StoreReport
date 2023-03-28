import pandas as pd 
import sys

def generate_features(df):
    # Creating column showing size of discount 
    df['discountPercentage'] = ((df['preSalePrice'] - df['price']) / df['preSalePrice']) * 100
    
    # Creating column showing product type 
    productType_List = []

    for product in df['name']:
        productType = product.strip()
        productType = productType.split()[-1]
        productType = productType.capitalize()
        productType_List.append(productType)

    df['productType'] = productType_List
    
    # If product type not in accepted types then set product type to accessory 
    acceptedTypes = ['Joggers', 'Shorts', 'T-shirt', 'Tank', 'Zip', 'Hoodie','Sweatshirt', 'Top', 
      'Stringer','Crew','Windbreaker','Legging','Leggings','Jacket','Tights', 'Short', 'Pullover',
     'Bra', 'Bralette','Pants','Bandeau','Cardigan','Bottoms','Gilet','B/c-e/f','Dress','Through','Jogger','Anorak', 'One']

    for i in range(len(df['productType'])):
        if df['productType'][i] not in (acceptedTypes): 
            df['productType'] = df['productType'].str.replace(df['productType'][i],'Other', regex=True)

        
    return df

def clean_data(df):
    # Delete rows with eGift Card
    df.drop(df.loc[df['name']=='eGift Card'].index, inplace=True)
    
    # Copy of Dataframe
    df_copy = df.copy()
    
    # Fills missing colors and fixes product name
    if df_copy['color'].isnull().any(): 
        df_copy = df_copy[df_copy['color'].isnull()]
        colors = [i.split('-')[1].strip() for i in df_copy['name']]
        df_copy['color'] = colors
        df_copy['name'] = [i.split('-')[0].strip() for i in df_copy['name']]

    df = pd.concat([df, df_copy], ignore_index = True)
    df = df.dropna(subset=['color'])

    return df

# Function to label items as accessories - items that were part of All Items in view for webpage
def apply_accessory_tag(df_original):
    df = df_original.copy()
    # Makes a list of the product type and category
    productType = list(df['productType'])
    category = list(df['category'])
    
    # Zips the two lists together
    newTag = pd.DataFrame(zip(productType,category), columns=['type','category'])
    
    # If there is a item that has type other, then label it as an accessory
    for i in range(len(newTag)):
        if newTag['type'][i] == 'Other':
            newTag['category'][i] = 'Accessory'
    
    # Use the new values and add it into the dataframe
    df['category'] = newTag['category']
    df['productType'] = newTag['type']
    
    return df
    
def main():
    # Reading in csv files
    df_mens = pd.read_csv('gymshark_mens.csv')
    df_womens = pd.read_csv('gymshark_womens.csv')
    df_accessories = pd.read_csv('gymshark_accessories.csv')

    #Adding new column -- category of clothing
    df_mens['category'] = 'Men'
    df_womens['category'] = 'Women'
    df_accessories['category'] = 'Accessory'
    
    df_mens = generate_features(df_mens)
    df_mens = apply_accessory_tag(df_mens)
    df_mens = clean_data(df_mens)
    
    df_womens = generate_features(df_womens)
    df_womens = apply_accessory_tag(df_womens)
    df_womens = clean_data(df_womens)
    
    df_accessories = generate_features(df_accessories)
    df_accessories = clean_data(df_accessories)
    
    # Merge dataframes
    dataframes = [df_mens, df_womens, df_accessories]
    df_gymshark = pd.concat(dataframes)
    df_gymshark = df_gymshark.drop_duplicates()

    df_gymshark['productType'] = df_gymshark['productType'].str.replace('Joggers','Jogger', regex=True)
    df_gymshark['productType'] = df_gymshark['productType'].str.replace('Leggings','Legging', regex=True)
    df_gymshark['productType'] = df_gymshark['productType'].str.replace('Otherigan','Cardigan', regex=True)
    df_gymshark['productType'] = df_gymshark['productType'].str.replace('Shorts','Short', regex=True)
    df_gymshark['productType'] = df_gymshark['productType'].str.replace('Short','Shorts', regex=True)
    df_gymshark['productType'] = df_gymshark['productType'].str.replace('One','Onesie', regex=True)
    
    # Name of csv file
    file_name = sys.argv[1]
    df_gymshark.to_csv(file_name, index = False)

main()