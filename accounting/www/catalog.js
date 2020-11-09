buyBtn = document.getElementById('buy-btn');
buyBtn.addEventListener('click', orderCart);

var api_req_headers = {
	'Content-Type': 'application/json',
};

if (window.csrf_token)
	api_req_headers['X-Frappe-CSRF-Token'] = window.csrf_token;

function addItemToCart(cart, item_qty) {
	item = item_qty.id;
	qty = item_qty.valueAsNumber;
	if (qty === 0) return;
	cart.items.push({ item: item, quantity: qty });
}

async function createSalesInvoice(cart) {
	const options = {
		method: 'POST',
		body: JSON.stringify(cart),
		headers: api_req_headers,
	};
	let url = document.location.origin + '/api/resource/Sales%20Invoice';
	fetch(url, options).then(validateResponse).then(showInvoicePDF);
}

function validateResponse(res) {
	if (res.ok) return res.json();
	showHTTPErr(res);
	return Promise.reject(res);
}

function showHTTPErr(res) {
	frappe.msgprint({
		title: 'HTTP Error: ' + res.status + ' ' + res.statusText,
		indicator: 'red',
		message: __('Something went wrong. Try again.'),
	});
}

function showInvoicePDF(res) {
	doc = res.data;
	let url =
		document.location.origin +
		'/api/method/frappe.utils.print_format.download_pdf?doctype=Sales%20Invoice&';
	url += 'name=' + doc.name + '&';
	url += 'format=Sales%20Invoice&no_letterhead=0&_lang=en';
	win = window.open(url, '_blank');
	win.focus();
}

async function getCustomer(user) {
	let url = document.location.origin + '/api/resource/Customer';
	url += '?filters=';
	url += '[["user", "=", "' + user + '" ]]';

	return fetch(url)
		.then(validateResponse)
		.then((res) => (res.data.length > 0 ? res.data[0].name : null));
}

async function createCustomer(user) {
	customer = { user: user };
	const options = {
		method: 'POST',
		body: JSON.stringify(customer),
		headers: api_req_headers,
	};
	let url = document.location.origin + '/api/resource/Customer';
	return fetch(url, options).then(validateResponse);
}

async function getUser() {
	let url =
		document.location.origin + '/api/method/frappe.auth.get_logged_user';
	return fetch(url)
		.then(validateResponse)
		.then((res) => res.message);
}

async function setCustomer(user) {
	customer = await getCustomer(user);
	if (!customer) customer = await createCustomer(user);
	return customer;
}

async function orderCart() {
	customer = await getUser().then(setCustomer);
	cart_item_qtys = document.querySelectorAll('.cart-item-qty');
	cart = {};
	cart.items = [];
	for (i = 0; i < cart_item_qtys.length; i++)
		addItemToCart(cart, cart_item_qtys[i]);
	if (cart.items.length === 0) {
		frappe.msgprint('Please add items to your cart');
		return;
	}
	cart.customer = customer;
	//to submit document
	cart.docstatus = true;
	await createSalesInvoice(cart);
}
