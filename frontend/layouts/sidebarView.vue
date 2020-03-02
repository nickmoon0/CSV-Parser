<template>		
	<div class="wrapper">
		<div class="sidebarWrap h-100">
			<nav id="sidebar" class="sidebarStyle h-100">
				<div class="sidebar-header">
					<h3>Menu</h3>
					<br/>
					<ul class="list-unstyled components">
						<li class="listElement">
							<nuxt-link to="/home">Home</nuxt-link>
						</li>
						<li class="listElement">
							<nuxt-link to="/upload">Upload File</nuxt-link>
						</li>
						<li class="listElement">
							<nuxt-link to="/errors">Errors</nuxt-link>
						</li>
						<div class="bottomText">
							<li class="listElement">
								<nuxt-link to="/accounts">Accounts</nuxt-link>
							</li>
							<li class="listElement">
								<nuxt-link to="/logout">Logout</nuxt-link>
							</li>
						</div>
					</ul>
				</div>
			</nav>
		</div>
		<nuxt/>
	</div>
</template>

<style>
</style>

<script>
export default {
	middleware: 'checkAuthenticated'
}
</script>
