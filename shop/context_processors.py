from django.urls import resolve
from django.utils.text import capfirst

def breadcrumbs(request):
    breadcrumbs = []
    path = request.path.strip("/").split("/")
    
    if not path or path == [""]:
        return {"breadcrumbs": [{"name": "Home", "url": "/"}]}

    # Build the breadcrumb list
    for index, part in enumerate(path):
        # Accumulate the URL for each segment
        url = "/" + "/".join(path[: index + 1])
        # Capitalize the name of each segment for display
        name = capfirst(part.replace("-", " "))
        breadcrumbs.append({"name": name, "url": url})

    # Include the homepage as the first breadcrumb
    breadcrumbs.insert(0, {"name": "Home", "url": "/"})
    
    return {"breadcrumbs": breadcrumbs}

