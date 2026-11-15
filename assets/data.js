// ---------------------------------------------------------------
// Family site data. Edit this file to update the site.
// ---------------------------------------------------------------

// Thanksgiving potluck: put a name in "by" when someone claims a dish.
// Example:  { name: "Pumpkin Pie", desc: "The classic", by: "Shibu" },
window.THANKSGIVING = {
  ours: [
    { name: "Herb-Roasted Turkey", desc: "Golden, juicy & the star of the table" },
    { name: "Homestyle Gravy", desc: "Rich pan gravy from the drippings" },
    { name: "Chicken Kondattam", desc: "Crispy chicken in a spicy, tangy chili-shallot masala", kerala: true },
    { name: "Grammie’s Nut Loaf", desc: "A savory, herb-packed vegetarian main" },
    { name: "Emma’s Mac & Cheese", desc: "Baked, bubbly & extra cheesy" },
    { name: "Green Bean Casserole", desc: "Creamy, with crispy fried onions" },
    { name: "Corn Casserole", desc: "Sweet, buttery & spoonable" },
    { name: "Cranberry Sauce", desc: "Sweet, tart & made fresh" },
    { name: "Herb Butter", desc: "Whipped with fresh herbs, made for warm rolls" }
  ],
  bring: [
    { name: "Appetizers", desc: "Something to nibble on before dinner", by: "" },
    { name: "Pappadam", desc: "Crisp, crackly & meant for passing", kerala: true, by: "" },
    { name: "Chicken Curry & Appam", desc: "Kerala curry with lacy rice hoppers", kerala: true, by: "" },
    { name: "Mashed Potatoes", desc: "Buttery & creamy", by: "" },
    { name: "Stuffing / Dressing", desc: "Cornbread, sage or a family recipe", by: "" },
    { name: "Sweet Potatoes", desc: "Casserole, roasted or candied — your call", by: "" },
    { name: "Vegetable Side", desc: "Salad, roasted veggies or a thoran", by: "" },
    { name: "Dinner Rolls", desc: "Soft & warm (the herb butter’s on us)", by: "" },
    { name: "Pumpkin Pie", desc: "The classic", by: "" },
    { name: "Whipped Cream", desc: "For topping the pies", by: "" },
    { name: "Dessert", desc: "Cake, cookies, brownies, payasam — surprise us", by: "" },
    { name: "Drinks", desc: "Cider, soda, chaya or your favorite", by: "" }
  ]
};

// Events: month is 1–12. Add "year" for one-time events; leave it off for yearly ones.
window.EVENTS = [
  { title: "Thanksgiving Dinner", detail: "6:00 PM · the whole family’s invited", month: 11, day: 26, year: 2026, link: "thanksgiving.html" },
  { title: "Gabriel’s Birthday", detail: "Yearly", month: 10, day: 8 },
  { title: "Emma’s Birthday", detail: "Yearly", month: 10, day: 6 },
  { title: "Evalyn’s Birthday", detail: "Yearly", month: 11, day: 3 },
  { title: "Abby’s Birthday", detail: "Yearly", month: 4, day: 27 },
  { title: "Abby & Shajan’s Anniversary", detail: "Yearly", month: 7, day: 1 }
];

// Family fundraiser. Fill these in once the family picks this year's cause.
// Leave "charity" empty to show "we're choosing" on the page.
window.FUNDRAISER = {
  year: 2026,
  charity: "",            // e.g. "Children's Healthcare of Atlanta"
  why: "",                // a sentence or two on why the family picked it
  goal: 0,                // dollars, e.g. 2500 (0 hides the goal)
  raised: 0,              // update by hand from GoFundMe (0 hides the progress bar)
  deadline: "December 31, 2026",
  gofundme: "",           // GoFundMe link
  charityLink: ""         // the charity's own donation page
};
// Add a line here each year once a fundraiser wraps up.
window.FUNDRAISER_PAST = [
  // { year: 2025, charity: "Name", raised: 1800 },
];
