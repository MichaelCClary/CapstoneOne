from forms import SearchForm


def get_collection_ids(user):
    ids = []
    if user:
        for game in user.collection:
            ids.append(game.api_id)

    return ids


def keep_data_searchform(searched, param, order):
    form = SearchForm()
    form.searchby.default = searched
    if searched == 'name':
        form.name.default = param
    form.mechanics.default = param
    form.categories.default = param
    form.min_players.default = param
    form.max_players.default = param
    form.order_by.default = order
    form.process()
    return form
