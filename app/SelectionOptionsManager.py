
class SelectionOptionsManager():

    def get_criterias():
        return [
            {'query_name': 'wine_servings', 'display_name': "Wine Servings"}, 
            {'query_name': 'beer_servings', 'display_name': "Beer Servings"},
            {'query_name': 'spirit_servings', 'display_name': "Spirit Servings"},
            {'query_name': 'total_litres_of_pure_alcohol','display_name': "Total Alcohol"},
            {'query_name': 'gpd_capita', 'display_name': "GPD"},
            {'query_name': 'population', 'display_name': 'Population'},
            {'query_name': 'area','display_name': "Area"}
        ]

    def get_options():
        return [
            {'query_name': 'ASC','display_name': "Ascending"}, 
            {'query_name': 'DESC','display_name': "Descending"}
        ]
    
    def get_filters():
        return [
            {'query_name': 'all','display_name': "Show All"},
            {'query_name': 'gt_avg','display_name': "Only Greater than Average"}, 
            {'query_name': 'gte_avg','display_name': "Greater or Equal Average"},
            {'query_name': 'lt_avg','display_name': "Only Less than Average"}, 
            {'query_name': 'lte_avg','display_name': "Less than or Equal Average"},
            {'query_name': 'eq_avg','display_name': "Equal Average"}, 
        ]