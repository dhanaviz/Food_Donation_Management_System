
import json
import os
from datetime import datetime

DONATIONS_FILE = "donations.json"
USERS_FILE = "users.json"


class FoodDonationSystem:

    def __init__(self):
        self.donations = self.load_data(DONATIONS_FILE)
        self.users = self.load_data(USERS_FILE)

    def load_data(self, filename):
        if not os.path.exists(filename):
            with open(filename, "w") as file:
                json.dump([], file)
            return []

        try:
            with open(filename, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Error reading", filename)
            return []

    def save_data(self):
        with open(DONATIONS_FILE, "w") as file:
            json.dump(self.donations, file, indent=4)

        with open(USERS_FILE, "w") as file:
            json.dump(self.users, file, indent=4)

    def add_user(self, user_id, name, role, contact):
        for user in self.users:
            if user["user_id"] == user_id:
                return

        self.users.append({
            "user_id": user_id,
            "name": name,
            "role": role,
            "contact": contact
        })

    def create_donation(self):
        try:
            print("\n========== CREATE DONATION ==========")

            donor_id = input("Enter Donor ID: ").strip()
            donor_name = input("Enter Donor Name: ").strip()
            contact = input("Enter Contact Number: ").strip()
            food = input("Enter Food Name: ").strip()
            quantity = int(input("Enter Quantity (Meals): "))
            location = input("Enter Location: ").strip()
            available_until = input("Available Until (e.g. 8:00 PM): ").strip()

            if not all([donor_id, donor_name, contact, food,
                        location, available_until]):
                print("Error: All fields are required.")
                return

            if quantity <= 0:
                print("Error: Quantity must be greater than zero.")
                return

            self.add_user(donor_id, donor_name, "Donor", contact)

            donation_id = "DON" + str(len(self.donations) + 1).zfill(3)

            donation = {
                "donation_id": donation_id,
                "donor_id": donor_id,
                "food_name": food,
                "quantity": quantity,
                "location": location,
                "available_until": available_until,
                "contact": contact,
                "status": "Available",
                "volunteer_id": None
            }

            self.donations.append(donation)
            self.save_data()

            print("\nDonation Created Successfully!")
            print("Donation ID:", donation_id)
            print("Status: Available")

        except ValueError:
            print("Error: Please enter a valid number for quantity.")

        except OSError:
            print("Error: Unable to save donation.")

    def view_donations(self):
        print("\n========== AVAILABLE DONATIONS ==========")

        available = [
            d for d in self.donations
            if d["status"] == "Available"
        ]

        if not available:
            print("No available donations.")
            return

        for d in available:
            print("--------------------------------")
            print("Donation ID :", d["donation_id"])
            print("Food        :", d["food_name"])
            print("Quantity    :", d["quantity"], "Meals")
            print("Location    :", d["location"])
            print("Available Until:", d["available_until"])
            print("Status      :", d["status"])

    def claim_donation(self):
        try:
            print("\n========== CLAIM DONATION ==========")

            donation_id = input("Enter Donation ID: ").strip()

            donation = next(
                (d for d in self.donations
                 if d["donation_id"] == donation_id),
                None
            )

            if donation is None:
                print("Error: Donation not found.")
                return

            if donation["status"] != "Available":
                print("Error: Donation is not available.")
                return

            volunteer_id = input("Enter Volunteer ID: ").strip()
            volunteer_name = input("Enter Volunteer Name: ").strip()
            contact = input("Enter Contact Number: ").strip()

            if not all([volunteer_id, volunteer_name, contact]):
                print("Error: All volunteer details are required.")
                return

            self.add_user(
                volunteer_id, volunteer_name, "Volunteer", contact
            )

            donation["status"] = "Claimed"
            donation["volunteer_id"] = volunteer_id

            self.save_data()

            print("\nDonation Successfully Claimed!")
            print("Donation ID:", donation_id)
            print("Status: Claimed")
            print("Volunteer:", volunteer_id)

        except OSError:
            print("Error: Unable to update donation.")

    def update_status(self, donation_id, new_status):
        donation = next(
            (d for d in self.donations
             if d["donation_id"] == donation_id),
            None
        )

        if donation is None:
            print("Error: Donation not found.")
            return

        allowed = {
            "Claimed": "Picked Up",
            "Picked Up": "Delivered"
        }

        if allowed.get(donation["status"]) != new_status:
            print("Error: Invalid status operation.")
            return

        donation["status"] = new_status
        self.save_data()

        print("Donation status updated successfully!")
        print("New Status:", new_status)

    def pickup_donation(self):
        print("\n========== PICKUP DONATION ==========")
        donation_id = input("Enter Donation ID: ").strip()
        self.update_status(donation_id, "Picked Up")

    def deliver_donation(self):
        print("\n========== DELIVER DONATION ==========")
        donation_id = input("Enter Donation ID: ").strip()
        self.update_status(donation_id, "Delivered")

    def view_all_records(self):
        print("\n========== ALL DONATION RECORDS ==========")

        if not self.donations:
            print("No donation records found.")
        else:
            for d in self.donations:
                print("--------------------------------")
                print("ID:", d["donation_id"])
                print("Food:", d["food_name"])
                print("Quantity:", d["quantity"], "Meals")
                print("Location:", d["location"])
                print("Donor:", d["donor_id"])
                print("Volunteer:", d["volunteer_id"])
                print("Status:", d["status"])

        print("\n========== USER RECORDS ==========")

        if not self.users:
            print("No user records found.")
        else:
            for user in self.users:
                print(
                    user["user_id"],
                    "|", user["name"],
                    "|", user["role"],
                    "|", user["contact"]
                )


def main():
    system = FoodDonationSystem()

    while True:
        print("\n======================================")
        print(" FOOD DONATION MANAGEMENT SYSTEM")
        print("======================================")
        print("1. Create Food Donation")
        print("2. View Available Donations")
        print("3. Claim Donation")
        print("4. Mark Donation as Picked Up")
        print("5. Mark Donation as Delivered")
        print("6. View All Records")
        print("7. Exit")
        print("======================================")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            system.create_donation()

        elif choice == "2":
            system.view_donations()

        elif choice == "3":
            system.claim_donation()

        elif choice == "4":
            system.pickup_donation()

        elif choice == "5":
            system.deliver_donation()

        elif choice == "6":
            system.view_all_records()

        elif choice == "7":
            print("Thank you for using Food Donation Management System!")
            break

        else:
            print("Invalid option! Please choose 1 to 7.")


if __name__ == "__main__":
    main()
