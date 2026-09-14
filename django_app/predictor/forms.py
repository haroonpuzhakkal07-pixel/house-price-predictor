from django import forms


class HousePredictionForm(forms.Form):
    # Property basics
    overall_qual = forms.IntegerField(
        label="Overall Quality",
        min_value=1,
        max_value=10,
        initial=5,
    )

    overall_cond = forms.IntegerField(
        label="Overall Condition",
        min_value=1,
        max_value=10,
        initial=5,
    )

    neighborhood = forms.CharField(
        label="Neighborhood",
        initial="CollgCr",
        max_length=50,
    )

    # Size
    gr_liv_area = forms.IntegerField(
        label="Above Ground Living Area (sq ft)",
        min_value=1,
        initial=1500,
    )

    total_bsmt_sf = forms.IntegerField(
        label="Basement Area (sq ft)",
        min_value=0,
        initial=800,
    )

    first_flr_sf = forms.IntegerField(
        label="First Floor Area (sq ft)",
        min_value=0,
        initial=1000,
    )

    second_flr_sf = forms.IntegerField(
        label="Second Floor Area (sq ft)",
        min_value=0,
        initial=500,
    )

    lot_area = forms.IntegerField(
        label="Lot Area (sq ft)",
        min_value=1,
        initial=8000,
    )

    # House age
    year_built = forms.IntegerField(
        label="Year Built",
        min_value=1800,
        max_value=2026,
        initial=2000,
    )

    year_remod_add = forms.IntegerField(
        label="Year Remodeled",
        min_value=1800,
        max_value=2026,
        initial=2000,
    )

    # Bathrooms / rooms
    full_bath = forms.IntegerField(
        label="Full Bathrooms",
        min_value=0,
        initial=2,
    )

    half_bath = forms.IntegerField(
        label="Half Bathrooms",
        min_value=0,
        initial=1,
    )

    bedroom_abv_gr = forms.IntegerField(
        label="Bedrooms Above Ground",
        min_value=0,
        initial=3,
    )

    tot_rms_abv_grd = forms.IntegerField(
        label="Total Rooms Above Ground",
        min_value=1,
        initial=6,
    )

    # Quality
    EXTER_QUAL_CHOICES = [
        ("Ex", "Excellent"),
        ("Gd", "Good"),
        ("TA", "Typical"),
        ("Fa", "Fair"),
        ("Po", "Poor"),
    ]

    KITCHEN_QUAL_CHOICES = [
        ("Ex", "Excellent"),
        ("Gd", "Good"),
        ("TA", "Typical"),
        ("Fa", "Fair"),
        ("Po", "Poor"),
    ]

    exter_qual = forms.ChoiceField(
        label="Exterior Quality",
        choices=EXTER_QUAL_CHOICES,
        initial="Gd",
    )

    kitchen_qual = forms.ChoiceField(
        label="Kitchen Quality",
        choices=KITCHEN_QUAL_CHOICES,
        initial="Gd",
    )

    # Garage
    garage_cars = forms.IntegerField(
        label="Garage Capacity (cars)",
        min_value=0,
        initial=2,
    )

    garage_area = forms.IntegerField(
        label="Garage Area (sq ft)",
        min_value=0,
        initial=400,
    )

    garage_yr_blt = forms.IntegerField(
        label="Garage Year Built",
        min_value=0,
        max_value=2026,
        initial=2000,
    )

    GARAGE_FINISH_CHOICES = [
        ("Fin", "Finished"),
        ("RFn", "Rough Finished"),
        ("Unf", "Unfinished"),
        ("NoFeature", "No Garage"),
    ]

    garage_finish = forms.ChoiceField(
        label="Garage Finish",
        choices=GARAGE_FINISH_CHOICES,
        initial="RFn",
    )

    # Basement
    BSMENT_QUAL_CHOICES = [
        ("Ex", "Excellent"),
        ("Gd", "Good"),
        ("TA", "Typical"),
        ("Fa", "Fair"),
        ("Po", "Poor"),
        ("NoFeature", "No Basement"),
    ]

    bsmt_qual = forms.ChoiceField(
        label="Basement Quality",
        choices=BSMENT_QUAL_CHOICES,
        initial="Gd",
    )

    # Sale information
    year_sold = forms.IntegerField(
        label="Year Sold",
        min_value=2006,
        max_value=2026,
        initial=2008,
    )

    month_sold = forms.IntegerField(
        label="Month Sold",
        min_value=1,
        max_value=12,
        initial=6,
    )