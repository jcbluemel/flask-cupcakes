/*

  click handler on form for submit button
  once submitted, save all form data in variables
  turn variables into JSON
  send axios (object) request to 'create_cupcake' route
  use return json to update list with the new cupcake (for id)

*/
"use strict";

const BASE_URL = "http://localhost:5000/";
const $cupcakeList = $("#cupcake-list");
const $addCupcakeForm = $("#add-cupcake");


async function addCupcake() {

  cupcakeInfo = getNewCupcakeInfo();
  cupcakeWithId = await addCupcakeToDatabase(cupcakeInfo);

  $cupcakeList.append(
    `<li>
      ${cupcakeInfo.flavor}
    </li>
    `
  )
}

function getNewCupcakeInfo() {

  const flavor = $("#flavor").val();
  const size = $("#size").val();
  const rating = $("#rating").val();
  const imageUrl = $("#image-url").val();

  return {
    flavor: flavor,
    size: size,
    rating: rating,
    image_url: imageUrl
  }
}

async function addCupcakeToDatabase(cupcakeInfo) {
  const response = await axios({
    baseURL: BASE_URL,
    url: `/api/cupcakes`,
    method: "POST",
    data: cupcakeInfo
  });

  let { cupcake } = response.data;
  return cupcake
}


$addCupcakeForm.on("submit", async function(evt) {
  evt.preventDefault();
  await addCupcake();
});