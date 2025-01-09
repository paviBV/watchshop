document.getElementById("search-bar").addEventListener("input", function () {
  const query = this.value;

  fetch(`/search_product/?q=${query}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Unable to fetch  data from search_product");
      }
      return response.json();
    })
    .then((data) => {
      console.log(data);
      const container = document.getElementById("product_list");
      container.innerHTML = "";
      const watches = data.results;
      console.log(watches);
      console.log(Array.isArray(watches));

      watches.forEach((watch) => {
        const watchDiv = document.createElement("div");
        watchDiv.classList.add("col-md-4");
        watchDiv.classList.add("mb-4");
        watchDiv.innerHTML = `
        <div class = "card" >
            <img src="${watch.image}" class="card-img-top" alt="${watch.name}"/>
            <div class="card-body">
            <h5 class="card-title">${watch.name}</h5>
            <p class="card-text">${watch.description} Price:${watch.price}</p>
            <a href="/product/${watch.id}" class="btn btn-primary">View</a>
            <a href="/editwatch/${watch.id}" class="btn btn-secondary">Edit</a>
            <a href="/deleteWatch/${watch.id}" class="btn btn-danger">Delete</a>
            </div>
        </div>
        `;
        container.appendChild(watchDiv);
      });
    })
    .catch((error) => {
      console.error("Error during search:", error);
    });
});
