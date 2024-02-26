import requests


class ActiveCampaign:
    class FieldValues:
        class FieldValue:
            def __init__(self, field, value, contact,cdate, udate, created_by, updated_by, links, id, owner):
                self.field=field
                self.value=value
                self.contact=contact
                self.cdate=cdate
                self.udate=udate
                self.created_by=created_by
                self.updated_by=updated_by
                self.links=links
                self.id=id
                self.owner=owner

        def __init__(self, data: list):
            self.field_values = [self.FieldValue(**i) for i in data]

        def get_field(self, field_id):
            for field in self.field_values:
                if field.field == field_id:
                    return field
            return None

    def __init__(self, api_key, domain):
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Api-Token": api_key,
        }
        self.url = f"https://{domain}/api/3/"

    def list_contacts(self, search_params: dict = None):
        url = f"{self.url}contacts{'?' if search_params else ''}{'&'.join([str(j)+'='+str(k) for j, k in search_params.items()])}"

        return requests.get(url, headers=self.headers)

    def get_field_values(self, contact_id):
        url = f"{self.url}/contacts/{contact_id}/fieldValues"

        field_values = requests.get(url, headers=self.headers)
        return self.FieldValues(field_values.json()["fieldValues"])

    def add_tag_to_contact(self, contact_id, tag_id):
        url = f"{self.url}contactTags"
        data = {"contactTag": {"contact": contact_id, "tag": tag_id}}

        return requests.post(url, headers=self.headers, json=data)

    def get_contact_tags(self, contact_id):
        url = f"{self.url}contacts/{contact_id}/contactTags"

        return requests.get(url, headers=self.headers)

    def delete_contact_tag(self, contact_tag_id):
        url = f"{self.url}contactTags/{contact_tag_id}"

        return requests.delete(url, headers=self.headers)

    def remove_tag_from_contact(self, contact_id, tag_id):
        contact_tags = self.get_contact_tags(contact_id).json()["contactTags"]
        if contact_tags:
            for tag in contact_tags:
                if tag["tag"] == tag_id:
                    return self.delete_contact_tag(tag["id"])
        return None

    def update_contact(self, contact_id, data):
        url = f"{self.url}contacts/{contact_id}"
        return requests.put(url, headers=self.headers, json=data)
