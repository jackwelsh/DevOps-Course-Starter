
import pytest
import requests
import json

from unittest.mock import patch
from datetime import date

from todo_app import create_app
from todo_app.index.trello import *
from todo_app.index.objects import *


class mock_trello_api:

    def get_cards():
        """
        mock cards data generated by running curl command
        curl -X GET "https://api.trello.com/1/boards//cards?key=&token=
        """

        cards = '''
        [
        {"id":"5fd61710b402d20f2e8c4802","checkItemStates":null,"closed":false,"dateLastActivity":"2020-12-13T13:28:48.876Z","desc":"","descData":null,"dueReminder":null,"idBoard":"5fd503d7e780f63e718bf593","idList":"5fd503e2db852a6e5a2fddab","idMembersVoted":[],"idShort":1,"idAttachmentCover":null,"idLabels":[],"manualCoverAttachment":false,"name":"Test","pos":65535,"shortLink":"ouOb3jQO","isTemplate":false,"cardRole":null,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":false,"votes":0,"viewingMemberVoted":false,"subscribed":false,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":null,"comments":0,"attachments":0,"description":false,"due":null,"dueComplete":false,"start":null},"dueComplete":false,"due":null,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/ouOb3jQO","start":null,"subscribed":false,"url":"https://trello.com/c/ouOb3jQO/1-test","cover":{"idAttachment":null,"color":null,"idUploadedBackground":null,"size":"normal","brightness":"light"}},
        {"id":"5ff1c3625610c040ffe2a1b3","checkItemStates":null,"closed":false,"dateLastActivity":"2021-01-03T13:15:14.945Z","desc":"","descData":null,"dueReminder":null,"idBoard":"5fd503d7e780f63e718bf593","idList":"5fd503e2db852a6e5a2fddab","idMembersVoted":[],"idShort":12,"idAttachmentCover":null,"idLabels":[],"manualCoverAttachment":false,"name":"Todo1","pos":131071,"shortLink":"8pobnhAn","isTemplate":false,"cardRole":null,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":false,"votes":0,"viewingMemberVoted":false,"subscribed":false,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":null,"comments":0,"attachments":0,"description":false,"due":null,"dueComplete":false,"start":null},"dueComplete":false,"due":null,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/8pobnhAn","start":null,"subscribed":false,"url":"https://trello.com/c/8pobnhAn/12-todo1","cover":{"idAttachment":null,"color":null,"idUploadedBackground":null,"size":"normal","brightness":"light"}},
        {"id":"5ff1c368a41789899e169053","checkItemStates":null,"closed":false,"dateLastActivity":"2021-01-03T13:15:20.051Z","desc":"","descData":null,"dueReminder":null,"idBoard":"5fd503d7e780f63e718bf593","idList":"5fd503e2db852a6e5a2fddab","idMembersVoted":[],"idShort":13,"idAttachmentCover":null,"idLabels":[],"manualCoverAttachment":false,"name":"Todo2","pos":196607,"shortLink":"3LnSrDts","isTemplate":false,"cardRole":null,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":false,"votes":0,"viewingMemberVoted":false,"subscribed":false,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":null,"comments":0,"attachments":0,"description":false,"due":null,"dueComplete":false,"start":null},"dueComplete":false,"due":null,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/3LnSrDts","start":null,"subscribed":false,"url":"https://trello.com/c/3LnSrDts/13-todo2","cover":{"idAttachment":null,"color":null,"idUploadedBackground":null,"size":"normal","brightness":"light"}},
        {"id":"5ff1c34e70659e719b9c3af0","checkItemStates":null,"closed":false,"dateLastActivity":"2021-01-03T13:14:54.299Z","desc":"","descData":null,"dueReminder":null,"idBoard":"5fd503d7e780f63e718bf593","idList":"5fd5044419980d052c5ba01a","idMembersVoted":[],"idShort":9,"idAttachmentCover":null,"idLabels":[],"manualCoverAttachment":false,"name":"Doing1","pos":65535,"shortLink":"P4g9Urdk","isTemplate":false,"cardRole":null,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":false,"votes":0,"viewingMemberVoted":false,"subscribed":false,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":null,"comments":0,"attachments":0,"description":false,"due":null,"dueComplete":false,"start":null},"dueComplete":false,"due":null,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/P4g9Urdk","start":null,"subscribed":false,"url":"https://trello.com/c/P4g9Urdk/9-doing1","cover":{"idAttachment":null,"color":null,"idUploadedBackground":null,"size":"normal","brightness":"light"}},
        {"id":"5ff1c3565a26824a98e82306","checkItemStates":null,"closed":false,"dateLastActivity":"2021-01-03T13:15:02.213Z","desc":"","descData":null,"dueReminder":null,"idBoard":"5fd503d7e780f63e718bf593","idList":"5fd5044419980d052c5ba01a","idMembersVoted":[],"idShort":10,"idAttachmentCover":null,"idLabels":[],"manualCoverAttachment":false,"name":"Doing2","pos":131071,"shortLink":"9OT0npwF","isTemplate":false,"cardRole":null,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":false,"votes":0,"viewingMemberVoted":false,"subscribed":false,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":null,"comments":0,"attachments":0,"description":false,"due":null,"dueComplete":false,"start":null},"dueComplete":false,"due":null,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/9OT0npwF","start":null,"subscribed":false,"url":"https://trello.com/c/9OT0npwF/10-doing2","cover":{"idAttachment":null,"color":null,"idUploadedBackground":null,"size":"normal","brightness":"light"}},
        {"id":"5ff1c3597a9f1e4b9785baca","checkItemStates":null,"closed":false,"dateLastActivity":"2021-01-03T13:15:05.303Z","desc":"","descData":null,"dueReminder":null,"idBoard":"5fd503d7e780f63e718bf593","idList":"5fd5044419980d052c5ba01a","idMembersVoted":[],"idShort":11,"idAttachmentCover":null,"idLabels":[],"manualCoverAttachment":false,"name":"Doing3","pos":196607,"shortLink":"cRClpz7i","isTemplate":false,"cardRole":null,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":false,"votes":0,"viewingMemberVoted":false,"subscribed":false,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":null,"comments":0,"attachments":0,"description":false,"due":null,"dueComplete":false,"start":null},"dueComplete":false,"due":null,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/cRClpz7i","start":null,"subscribed":false,"url":"https://trello.com/c/cRClpz7i/11-doing3","cover":{"idAttachment":null,"color":null,"idUploadedBackground":null,"size":"normal","brightness":"light"}},
        {"id":"5feca5e4cb27193919ca8fc5","checkItemStates":null,"closed":false,"dateLastActivity":"2020-12-30T16:08:04.828Z","desc":"","descData":null,"dueReminder":null,"idBoard":"5fd503d7e780f63e718bf593","idList":"5fd50448c2dc7974d2abed4b","idMembersVoted":[],"idShort":2,"idAttachmentCover":null,"idLabels":[],"manualCoverAttachment":false,"name":"Done1","pos":65535,"shortLink":"xNE8kOdD","isTemplate":false,"cardRole":null,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":false,"votes":0,"viewingMemberVoted":false,"subscribed":false,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":null,"comments":0,"attachments":0,"description":false,"due":null,"dueComplete":false,"start":null},"dueComplete":false,"due":null,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/xNE8kOdD","start":null,"subscribed":false,"url":"https://trello.com/c/xNE8kOdD/2-done1","cover":{"idAttachment":null,"color":null,"idUploadedBackground":null,"size":"normal","brightness":"light"}},
        {"id":"5feca5e90e80462159a90be3","checkItemStates":null,"closed":false,"dateLastActivity":"2020-12-30T16:08:09.971Z","desc":"","descData":null,"dueReminder":null,"idBoard":"5fd503d7e780f63e718bf593","idList":"5fd50448c2dc7974d2abed4b","idMembersVoted":[],"idShort":3,"idAttachmentCover":null,"idLabels":[],"manualCoverAttachment":false,"name":"Done2","pos":131071,"shortLink":"9srD0VRg","isTemplate":false,"cardRole":null,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":false,"votes":0,"viewingMemberVoted":false,"subscribed":false,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":null,"comments":0,"attachments":0,"description":false,"due":null,"dueComplete":false,"start":null},"dueComplete":false,"due":null,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/9srD0VRg","start":null,"subscribed":false,"url":"https://trello.com/c/9srD0VRg/3-done2","cover":{"idAttachment":null,"color":null,"idUploadedBackground":null,"size":"normal","brightness":"light"}},
        {"id":"5feca5f1ea090949f317af96","checkItemStates":null,"closed":false,"dateLastActivity":"2020-12-30T16:08:17.632Z","desc":"","descData":null,"dueReminder":null,"idBoard":"5fd503d7e780f63e718bf593","idList":"5fd50448c2dc7974d2abed4b","idMembersVoted":[],"idShort":4,"idAttachmentCover":null,"idLabels":[],"manualCoverAttachment":false,"name":"Done3","pos":196607,"shortLink":"YPboQyw0","isTemplate":false,"cardRole":null,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":false,"votes":0,"viewingMemberVoted":false,"subscribed":false,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":null,"comments":0,"attachments":0,"description":false,"due":null,"dueComplete":false,"start":null},"dueComplete":false,"due":null,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/YPboQyw0","start":null,"subscribed":false,"url":"https://trello.com/c/YPboQyw0/4-done3","cover":{"idAttachment":null,"color":null,"idUploadedBackground":null,"size":"normal","brightness":"light"}},
        {"id":"5feca5fe90b3533211957225","checkItemStates":null,"closed":false,"dateLastActivity":"2020-12-30T16:08:30.276Z","desc":"","descData":null,"dueReminder":null,"idBoard":"5fd503d7e780f63e718bf593","idList":"5fd50448c2dc7974d2abed4b","idMembersVoted":[],"idShort":5,"idAttachmentCover":null,"idLabels":[],"manualCoverAttachment":false,"name":"Done4","pos":262143,"shortLink":"HsLEp764","isTemplate":false,"cardRole":null,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":false,"votes":0,"viewingMemberVoted":false,"subscribed":false,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":null,"comments":0,"attachments":0,"description":false,"due":null,"dueComplete":false,"start":null},"dueComplete":false,"due":null,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/HsLEp764","start":null,"subscribed":false,"url":"https://trello.com/c/HsLEp764/5-done4","cover":{"idAttachment":null,"color":null,"idUploadedBackground":null,"size":"normal","brightness":"light"}},
        {"id":"5feca603641fc384843aed66","checkItemStates":null,"closed":false,"dateLastActivity":"2020-12-30T16:08:35.597Z","desc":"","descData":null,"dueReminder":null,"idBoard":"5fd503d7e780f63e718bf593","idList":"5fd50448c2dc7974d2abed4b","idMembersVoted":[],"idShort":6,"idAttachmentCover":null,"idLabels":[],"manualCoverAttachment":false,"name":"Done5","pos":327679,"shortLink":"h97mNEc8","isTemplate":false,"cardRole":null,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":false,"votes":0,"viewingMemberVoted":false,"subscribed":false,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":null,"comments":0,"attachments":0,"description":false,"due":null,"dueComplete":false,"start":null},"dueComplete":false,"due":null,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/h97mNEc8","start":null,"subscribed":false,"url":"https://trello.com/c/h97mNEc8/6-done5","cover":{"idAttachment":null,"color":null,"idUploadedBackground":null,"size":"normal","brightness":"light"}},
        {"id":"5feca6078f88ec4fba621296","checkItemStates":null,"closed":false,"dateLastActivity":"2020-12-29T16:08:39.489Z","desc":"","descData":null,"dueReminder":null,"idBoard":"5fd503d7e780f63e718bf593","idList":"5fd50448c2dc7974d2abed4b","idMembersVoted":[],"idShort":7,"idAttachmentCover":null,"idLabels":[],"manualCoverAttachment":false,"name":"Done6","pos":393215,"shortLink":"Ferb54WM","isTemplate":false,"cardRole":null,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":false,"votes":0,"viewingMemberVoted":false,"subscribed":false,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":null,"comments":0,"attachments":0,"description":false,"due":null,"dueComplete":false,"start":null},"dueComplete":false,"due":null,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/Ferb54WM","start":null,"subscribed":false,"url":"https://trello.com/c/Ferb54WM/7-done6","cover":{"idAttachment":null,"color":null,"idUploadedBackground":null,"size":"normal","brightness":"light"}},
        {"id":"5feca60a6174285cd6f17b5a","checkItemStates":null,"closed":false,"dateLastActivity":"2020-12-28T16:08:42.698Z","desc":"","descData":null,"dueReminder":null,"idBoard":"5fd503d7e780f63e718bf593","idList":"5fd50448c2dc7974d2abed4b","idMembersVoted":[],"idShort":8,"idAttachmentCover":null,"idLabels":[],"manualCoverAttachment":false,"name":"Done7","pos":458751,"shortLink":"tVynx2Kv","isTemplate":false,"cardRole":null,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":false,"votes":0,"viewingMemberVoted":false,"subscribed":false,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":null,"comments":0,"attachments":0,"description":false,"due":null,"dueComplete":false,"start":null},"dueComplete":false,"due":null,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/tVynx2Kv","start":null,"subscribed":false,"url":"https://trello.com/c/tVynx2Kv/8-done7","cover":{"idAttachment":null,"color":null,"idUploadedBackground":null,"size":"normal","brightness":"light"}}
        ]
        '''
        return json.loads(cards)

    def get_card():
        """
        mock card data generated by running curl command
        curl -X GET "https://api.trello.com/1/cards/?key=&token="

        """
        card = '{"id": "5f835afcf6400f7c70f9597e", "checkItemStates": [], "closed": false, "dateLastActivity": "2020-10-11T19:20:28.624Z", "desc": "This is a test task for a new item", "descData": null, "dueReminder": null, "idBoard": "5fd503d7e780f63e718bf593", "idList": "5fd503e2db852a6e5a2fddab", "idMembersVoted": [], "idShort": 63, "idAttachmentCover": null, "idLabels": [], "manualCoverAttachment": false, "name": "New Test Task", "pos": 32768, "shortLink": "iUihslfg", "isTemplate": false, "dueComplete": false, "due": "2020-10-30T00:00:00.000Z", "labels": [], "shortUrl": "https://trello.com/c/iUihslfg", "start": null,"url": "https://trello.com/c/iUihslfg/63-new-test-task", "cover": {"idAttachment": null, "color": null, "idUploadedBackground": null, "size": "normal", "brightness": "light"}, "idMembers": [], "email": null, "badges": {"attachmentsByType": {"trello": {"board": 0, "card": 0}}, "location": false, "votes": 0, "viewingMemberVoted": false, "subscribed": false, "fogbugz": "", "checkItems": 0, "checkItemsChecked": 0, "checkItemsEarliestDue": null, "comments": 0, "attachments": 0, "description": true, "due": "2020-10-30T00:00:00.000Z", "dueComplete": false, "start": null}, "subscribed": false, "idChecklists": []}'
        return json.loads(card)

    def get_lists():
        """
        mock list data generated by running curl command
        curl -X GET "https://api.trello.com/1/boards/+self.board+/lists/?key=&token="
        """
        lists = '''
        [
            {"id": "5fd503e2db852a6e5a2fddab", "name": "TODO", "closed": false, "pos": 65535,"softLimit": null, "idBoard": "5fd503d7e780f63e718bf593", "subscribed": false},
            {"id": "5fd5044419980d052c5ba01a", "name": "DOING", "closed": false, "pos": 131071,"softLimit": null, "idBoard": "5fd503d7e780f63e718bf593", "subscribed": false},
            {"id": "5fd50448c2dc7974d2abed4b", "name": "DONE", "closed": false, "pos": 196607,"softLimit": null, "idBoard": "5fd503d7e780f63e718bf593", "subscribed": false}
        ]
        '''
        return json.loads(lists)


@pytest.fixture
def lists():
    # setup()
    mock_lists = mock_trello_api.get_lists()
    lists = [List(k, i) for i, k in enumerate(mock_lists)]
    yield lists


def test_list_id(lists):
    assert lists[0].id == "5fd503e2db852a6e5a2fddab"


@pytest.fixture
def card():
    # setup()
    mock_card = mock_trello_api.get_card()
    mock_list = [List(k, i) for i, k in enumerate(mock_trello_api.get_lists())]
    card = Card(mock_list, mock_card)
    yield card


@pytest.fixture
def cards():
    # setup()
    mock_cards = mock_trello_api.get_cards()
    mock_list = [List(k, i) for i, k in enumerate(mock_trello_api.get_lists())]
    cards = [Card(mock_list, i) for i in mock_cards]
    yield cards


@pytest.fixture
def done_card(cards):
    mock_done_card = [i for i in cards if i.listName == "DONE"][0]
    yield mock_done_card


def test_card_id(card):
    assert card.id == "5f835afcf6400f7c70f9597e"


def test_card_name(card):
    assert card.name == "New Test Task"


def test_card_list_id(card):
    assert card.listId == "5fd503e2db852a6e5a2fddab"


def test_card_list_name(card):
    assert card.listName == "TODO"


def test_card_due(card):
    assert card.due == "2020-10-30"


def test_card_date_last_activity(card):
    assert card.dateLastActivity == "2020-10-11"


def test_done_card(done_card):
    assert done_card.listName == "DONE"


class MockViewModel(ViewModel):
    def get_date(self):
        return date.fromisoformat("2020-12-30").strftime("%Y-%m-%d")


@pytest.fixture
def card_view_model(cards, lists):
    yield MockViewModel(cards, lists)


def test_view_model_get_date_mock(card_view_model):
    assert card_view_model.get_date() == "2020-12-30"


def test_view_model_show_all_done_cards(card_view_model):
    v = card_view_model.show_all_done_items
    assert v == False


def test_view_model_recent_done_items(card_view_model):
    v = card_view_model.recent_done_items
    assert len(v) == 5


def test_view_model_older_done_items(card_view_model):
    v = card_view_model.older_done_items
    assert len(v) == 2
