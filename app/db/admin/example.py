from sqladmin import ModelView

from app.db.models.example import Example


class ExampleAdmin(ModelView, model=Example):
    column_list = "__all__"
    column_searchable_list = [Example.name]
    column_sortable_list = [str(Example.id), Example.name, str(Example.created_at)]
