import json
import csv
from datetime import date
from django.shortcuts import render
from django.http import HttpResponse

def submit_data(request):
    if request.method == 'POST':
        # Get data from the form
        company_name = request.POST.get('company_name')
        quote = request.POST.get('quote')
        buy_price = float(request.POST.get('buy_price'))
        quantity = int(request.POST.get('quantity'))
        buy_total_price_with_BRK = int(request.POST.get('buy_total_price_with_BRK'))
        buy_order_price = buy_price * quantity
        BRK_Buy_charge = buy_total_price_with_BRK - buy_order_price
        sell_price = float(request.POST.get('sell_price'))
        sell_total_price_with_BRK = quantity * sell_price
        sell_order_price = int(request.POST.get('sell_order_price'))
        BRK_Sell_charge = sell_total_price_with_BRK - sell_order_price
        total_brk_charge = BRK_Buy_charge + BRK_Sell_charge
        profit_or_loss = (sell_total_price_with_BRK - buy_total_price_with_BRK) - total_brk_charge

        # Create a dictionary with the collected data
        data = {
            'date': str(date.today()),
            'company_name': company_name,
            'quote': quote,
            'buy_price': buy_price,
            'quantity': quantity,
            'buy_total_price_with_BRK': buy_total_price_with_BRK,
            'buy_order_price': buy_order_price,
            'BRK_Buy_charge': BRK_Buy_charge,
            'sell_price': sell_price,
            'sell_total_price_with_BRK': sell_total_price_with_BRK,
            'sell_order_price': sell_order_price,
            'BRK_Sell_charge': BRK_Sell_charge,
            'total_brk_charge': total_brk_charge,
            'profit_or_loss': profit_or_loss,
        }

        # Generate JSON file with the data
        with open('data.json', 'a') as json_file:
            json.dump(data, json_file, indent=4)
            json_file.write('\n')


        # Update/Append data to CSV file
        with open('data.csv', 'a', newline='') as csv_file:
            fieldnames = ['date', 'company_name', 'quote', 'buy_price', 'quantity', 'buy_total_price_with_BRK',
                          'buy_order_price', 'BRK_Buy_charge', 'sell_price', 'sell_total_price_with_BRK',
                          'sell_order_price', 'BRK_Sell_charge', 'total_brk_charge', 'profit_or_loss']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if csv_file.tell() == 0:  # If file is empty, write headers
                writer.writeheader()
            writer.writerow(data)

        return HttpResponse('Data submitted successfully!')


    return render(request, 'index.html')


def view_content(request):
    # Read the data from data.csv
    content = []
    with open('data.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            content.append(row)

    return render(request, 'view_content.html', {'content': content})


