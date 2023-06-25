var beurl = 'https://10.0.2.2:8000'

var api = {
	getLogin(username, password){
		var loginpg = beurl.concat('/user/login/');
		return fetch(loginpg, {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				username: username,
				password: password
			})
		}).then((res) => res.json());
	},
	getUserInfo(username, token){
		var userinfopg = beurl.concat(
			'/user/userinfo/',
			'?Auth=',
			token,
			'&username=',
			username
		);
		return fetch(userinfopg, {
			method: 'GET'
		}).then((res) => res.json());
	},
	logoutUser(token){
		var userlogout = beurl.concat(
			'/user/logout/',
			'?Auth=',
			token
		);
		return fetch(userlogout, {
			method: 'GET'
		}).then((res) => res.json());
	},
	useravail(username){
		var useravail = beurl.concat(
			'/user/usernameavailcheck/',
			'?username_req=',
			username
		);
		return fetch(useravail, {
			method: 'GET'
		}).then((res) => res.json());
	},
	createUser(infolist){
		var userform = beurl.concat('/user/create_account/');
		return fetch(userform, {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(infolist)
		}).then((res) => res.json());
	},
	obtainQuests(username, token){
		var questobtain = beurl.concat(
			'/submit/quest/',
			'?Auth=',
			token,
			'&username=',
			username
		);
		return fetch(questobtain, {
			method: 'GET'
		}).then((res) => res.json());
	},
	playerInfo(username, token){
		var questobtain = beurl.concat(
			'/player/info/',
			'?Auth=',
			token,
			'&username=',
			username
		);
		return fetch(questobtain, {
			method: 'GET'
		}).then((res) => res.json());
	},
	submitQuest(username, token, questno, picture) {
		var submitquest = beurl.concat('/submit/');
		var formsubmit = new FormData();
		formsubmit.append('username', username);
		formsubmit.append('Auth', token);
		formsubmit.append('Quest', questno);
		formsubmit.append('submit', picture);
		return fetch(submitquest, {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'multipart/form-data',
			},
			body: formsubmit
		}).then((res) => res.json());
	},
	updateUser(infolist){
		var userform = beurl.concat('/user/update_account/');
		return fetch(userform, {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'multipart/form-data',
			},
			body: infolist
		}).then((res) => res.json());
	},
	deleteUser(username, token, password){
		var deleteacc = beurl.concat('/user/delete_account/')
		var formsubmit = new FormData();
		formsubmit.append('username', username);
		formsubmit.append('password', password);
		formsubmit.append('Auth', token);
		return fetch(deleteacc, {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'multipart/form-data',
			},
			body: formsubmit
		}).then((res) => res.json());
	},
	changePassword(username, token, oldpassword, password1, password2){
		var cpass = beurl.concat('/user/change_password/');
		var fs = new FormData();
		fs.append('username', username);
		fs.append('Auth', token);
		fs.append('oldpassword', oldpassword);
		fs.append('password1', password1);
		fs.append('password2', password2);
		return fetch(cpass, {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'multipart/form-data',
			},
			body: fs
		}).then((res) => res.json());
	},
	getLeaderboard(){
		var lbcall = beurl.concat('/player/lb/');
		return fetch(lbcall, {
			method: 'GET',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'multipart/form-data',
			}
		}).then((res) => res.json());
	},
};

module.exports = api;
