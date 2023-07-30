import json
import csv
from datetime import date, datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse

def calculate_total(data_list):
    # Calculate the total of all numeric fields across all rows
    total_row = {
        'date': "Total",
        'company_name': "",
        'quote': "",
        'buy_price': sum(item['buy_price'] for item in data_list),
        'quantity': sum(item['quantity'] for item in data_list),
        'buy_total_price_with_BRK': sum(item['buy_total_price_with_BRK'] for item in data_list),
        'buy_order_price': sum(item['buy_order_price'] for item in data_list),
        'BRK_Buy_charge': sum(item['BRK_Buy_charge'] for item in data_list),
        'sell_price': sum(item['sell_price'] for item in data_list),
        'sell_total_price_with_BRK': sum(item['sell_total_price_with_BRK'] for item in data_list),
        'sell_order_price': sum(item['sell_order_price'] for item in data_list),
        'BRK_Sell_charge': sum(item['BRK_Sell_charge'] for item in data_list),
        'total_brk_charge': sum(item['total_brk_charge'] for item in data_list),
        'profit_or_loss': sum(item['profit_or_loss'] for item in data_list),
    }
    return total_row

def submit_data(request):
    if request.method == 'POST':
        # Get data from the form
        company_name = request.POST.get('company_name')
        quote = request.POST.get('quote')
        buy_price = float(round(float(request.POST.get('buy_price')), 2))
        quantity = int(request.POST.get('quantity'))
        buy_total_price_with_BRK = float(round(float(request.POST.get('buy_total_price_with_BRK')), 2))
        buy_order_price = float(round(buy_price * quantity, 2))
        BRK_Buy_charge = float(round(buy_total_price_with_BRK - buy_order_price, 2))
        sell_price = float(round(float(request.POST.get('sell_price')), 2))
        sell_total_price_with_BRK = float(round(quantity * sell_price, 2))
        sell_order_price = float(round(float(request.POST.get('sell_order_price')), 2))
        BRK_Sell_charge = float(round(sell_total_price_with_BRK - sell_order_price, 2))
        total_brk_charge = float(round(BRK_Buy_charge + BRK_Sell_charge, 2))
        profit_or_loss = float(round((sell_total_price_with_BRK - buy_total_price_with_BRK) - total_brk_charge, 2))

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

        try:
            # Check if data.json exists and contains valid JSON data
            with open('data.json', 'r') as json_file:
                data_list = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or has invalid JSON, start with an empty list
            data_list = []

        # Append the new data to the list
        data_list.append(data)

        # Write the updated data back to data.json
        with open('data.json', 'w') as json_file:
            json.dump(data_list, json_file, indent=4)

        # Calculate the total row
        total_row = calculate_total(data_list)

        # Write the updated data (including the total row) back to data.json
        with open('data.json', 'w') as json_file:
            json.dump(data_list + [total_row], json_file, indent=4)

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
    # Read the data from data.json
    try:
        with open('data.json', 'r') as json_file:
            content = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        content = []

    return render(request, 'view_content.html', {'content': content})


def modify(request):
    if request.method == 'POST':
        # Get selected date from the form
        selected_date = request.POST.get('selected_date')

        # Read the data from data.json
        try:
            with open('data.json', 'r') as json_file:
                data = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        # Get all companies from the selected date
        companies_on_date = [item['company_name'] for item in data if item['date'] == selected_date]

        return render(request, 'modify.html', {'companies': companies_on_date})

    return render(request, 'index.html')


def edit_company(request):
    if request.method == 'POST':
        # Get selected company from the form
        selected_company = request.POST.get('company')

        # Read the data from data.json
        try:
            with open('data.json', 'r') as json_file:
                data = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        # Find the selected company data
        company_data = {}
        for item in data:
            if item['company_name'] == selected_company:
                company_data = item
                break

        return render(request, 'edit_company.html', {'company_data': company_data})

    return render(request, 'modify.html')


def update_company(request):
    if request.method == 'POST':
        # Get data from the form
        company_name = request.POST.get('company_name')
        quote = request.POST.get('quote')
        buy_price = float(round(float(request.POST.get('buy_price')), 2))
        quantity = int(request.POST.get('quantity'))
        buy_total_price_with_BRK = float(round(float(request.POST.get('buy_total_price_with_BRK')), 2))
        buy_order_price = float(round(buy_price * quantity, 2))
        BRK_Buy_charge = float(round(buy_total_price_with_BRK - buy_order_price, 2))
        sell_price = float(round(float(request.POST.get('sell_price')), 2))
        sell_total_price_with_BRK = float(round(quantity * sell_price, 2))
        sell_order_price = float(round(float(request.POST.get('sell_order_price')), 2))
        BRK_Sell_charge = float(round(sell_total_price_with_BRK - sell_order_price, 2))
        total_brk_charge = float(round(BRK_Buy_charge + BRK_Sell_charge, 2))
        profit_or_loss = float(round((sell_total_price_with_BRK - buy_total_price_with_BRK) - total_brk_charge, 2))

        # Read the data from data.json
        try:
            with open('data.json', 'r') as json_file:
                data = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        # Find the selected company data and update it
        for item in data:
            if item['company_name'] == company_name:
                item['quote'] = quote
                item['buy_price'] = buy_price
                item['quantity'] = quantity
                item['buy_total_price_with_BRK'] = buy_total_price_with_BRK
                item['buy_order_price'] = buy_order_price
                item['BRK_Buy_charge'] = BRK_Buy_charge
                item['sell_price'] = sell_price
                item['sell_total_price_with_BRK'] = sell_total_price_with_BRK
                item['sell_order_price'] = sell_order_price
                item['BRK_Sell_charge'] = BRK_Sell_charge
                item['total_brk_charge'] = total_brk_charge
                item['profit_or_loss'] = profit_or_loss
                item['update_date'] = str(datetime.now().date())  # Update the "update_date" field
                break

        # Write the updated data back to data.json
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

        return redirect('view_content')

    return render(request, 'modify.html')
