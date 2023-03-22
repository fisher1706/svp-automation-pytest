class Account:

    def __init__(self, en_name, ar_name, logo, country, country_id, country_code, category, city, address, postal_code,
                 contact_name, sub_number, phone_number, email, show_logo=False):
        self.en_name = en_name
        self.ar_name = ar_name
        self.logo = logo
        self.country = country
        self.country_id = country_id
        self.country_code = country_code
        self.category = category
        self.city = city
        self.address = address
        self.postal_code = postal_code
        self.contact_name = contact_name
        self.sub_number = sub_number
        self.phone_number = phone_number
        self.email = email
        self.show_logo = show_logo
