buyBtn = document.getElementById('buy-btn');
buyBtn.addEventListener('click', orderCart);

function addItemToCart(cart, item_qty) {
	item = item_qty.id;
	qty = item_qty.valueAsNumber;
	cart.items.push({ item: item, quantity: qty });
}

function createSalesInvoice(cart) {
	const options = {
		method: 'POST',
		body: JSON.stringify(cart),
		headers: {
			'Content-Type': 'application/json',
		},
	};
	if (window.csrf_token) {
		options.headers['X-Frappe-CSRF-Token'] = window.csrf_token;
		console.log('csrf_token is ' + window.csrf_token);
		console.log(JSON.stringify(cart));
	}
	const url = document.location.origin + '/api/resource/Sales%20Invoice';
	fetch(url, options)
		.then((res) => res.json())
		.then(showInvoicePDF);
}

function showError(res) {
	return frappe.msgprint({
		title: __('Error'),
		indicator: 'red',
		message: __('Something went wrong. Try again.'),
	});
}

function showInvoicePDF(res) {
	doc = res.data
	let url =
		document.location.origin +
		'/api/method/frappe.utils.print_format.download_pdf?doctype=Sales%20Invoice&';
	url += 'name=' + doc.name + '&';
	url += 'format=Sales%20Invoice&no_letterhead=0&_lang=en';
	win = window.open(url, '_blank');
  win.focus();
}

function orderCart() {
	cart_item_qtys = document.querySelectorAll('.cart-item-qty');
	cart = {};
	cart.items = [];
	for (i = 0; i < cart_item_qtys.length; i++) {
		addItemToCart(cart, cart_item_qtys[i]);
	}
	cart.customer = 'balu';
	//to submit document
	cart.docstatus = true;
	createSalesInvoice(cart);
}
