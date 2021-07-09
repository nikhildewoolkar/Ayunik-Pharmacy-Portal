package com.SwapTreasure.app;

import java.util.ArrayList;
import java.util.List;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.web.bind.annotation.PostMapping;

@Configuration
@EnableWebSecurity
public class AppSec extends WebSecurityConfigurerAdapter{

	@Bean
	@Override
	protected UserDetailsService userDetailsService() {
		List<UserDetails> users = new ArrayList<>();
		users.add(User.withDefaultPasswordEncoder().username("nikhildewoolkar29").password("12345").roles("USER").build());
		users.add(User.withDefaultPasswordEncoder().username("nikhildewoolkar29").password("12345").roles("USER").build());
		users.add(User.withDefaultPasswordEncoder().username("admin").password("123").roles("USER").build());
		return new InMemoryUserDetailsManager(users);
	}


	
}
