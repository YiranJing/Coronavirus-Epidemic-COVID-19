	# Jonathan Read, Jessica Bridgen, Chris Jewell, Jan 2020
	# Lancaster University
	# email: jonathan.read@lancaster.ac.uk 

	rm( list=ls() )
	sf = function() { source( "epidemic modelling functions.R" ) }
	sf()
	
	# import flight data
		# OAG propriatorial data
		K1 = import.matrix("China_domestic_flight_network.csv") # domestic
		K2 = import.matrix("China_international_flight_network.csv") # international
		# account for monthly data, convert to daily
		K1 = K1/31
		K2 = K2/31
		city.seq = rownames(K1)
		m = length(city.seq)
		w = ncol(K2) # number of other countries
		country.seq = colnames(K2)
		# connectivity of Wuhan to China cities
			sum(K1[151,]*31)
			sort(K1[151,]*31, decreasing=TRUE)[1:3]
		# connectivity of Wuhan internationally
			sum(K2[151,]*31)
			sort(K1[151,]*31, decreasing=TRUE)[1:3]
			
		
	# import incidence data
		obs = list(
			data_China = import.matrix("data_China_2019-nCoV.csv", replace.NA.w.zero=TRUE),
			data_World = import.matrix("data_World_2019-nCoV.csv", replace.NA.w.zero=TRUE)
		)
		rownames( obs$data_China ) = city.seq # account for google character mangling
		
	# import population data
		pop = read.csv( "China city population data.csv" )
		N = pop$City.Population
		names(N) = city.seq # google sheets mangled some accented characters
		
	
	# fitting
		param.init = c(
			0.4, # beta_1
			1/7, # gamma
			0.5, # phi
			1	 # I0W
		)
		alpha = 1/4 # SARS, see Lessler 2009
		t.max = 20 # 21 Jan 2020
	
		hess = optim( log(param.init), 
			logLikelihood, 
			obs=obs, 
			alpha=alpha,
			t.max=t.max, 
			K1=K1, K2=K2,
			control=list(fnscale=-1),
			hessian=TRUE
		)
		# Covariance matrix
		V = solve(-hess$hessian)
		colnames(V)=rownames(V)=c("beta_1","gamma","phi","I0W")
		print(V)
		
		# parameters
			param = make.param( hess )
		# R0 estimation
			print.R0( param )
		# Infectious period estimation
			print.InfP( param )
		

	# sensitivity to alpha (and incubation period)
		# Lessler 4.0 days (95% CI 3.6-4.4)
		hess.alpha.lo = optim( log(param.init), 
			logLikelihood, 
			obs=obs, 
			alpha=1/3.6,
			t.max=t.max, 
			K1=K1, K2=K2,
			control=list(fnscale=-1),
			hessian=TRUE,
			method = "Nelder-Mead"
		)	
		hess.alpha.hi = optim( log(param.init), 
			logLikelihood, 
			obs=obs, 
			alpha=1/4.4,
			t.max=t.max, 
			K1=K1, K2=K2,
			control=list(fnscale=-1),
			hessian=TRUE,
			method = "Nelder-Mead"
		)
		dev.new(width=10, height=2)
			plot.alpha.sensitivity( hess, hess.alpha.lo, hess.alpha.hi )	
		dev.copy2pdf( file="fig_sensitivity_alpha.pdf", useDingbats=FALSE )
		dev.off()
		
	
	# simulation using fitted values
		t.now = t.max
		t.plus = 14 # take it to the start of March
		date.seq = seq( 
			from=as.Date("2020-01-01"),
			to=as.Date("2020-01-01")+t.now+t.plus,
			by=1 
		)
		a = epidemic.sim( 
			beta_1=param$value[1], 
			gamma=param$value[2], 
			alpha=1/4, 
			phi=param$value[3], 
			I0W=param$value[4],
			t.max=t.now+t.plus,
			K1, K2
		)
		phi = param$value[3]
		
		# what size of outbreak do we currently have in Wuhan?
		# number of infections occured and current in Wuhan and elsewhere in China.
			T = t.now
			Tend = length( date.seq )
			repl.max = 500
			wuhan.infections = numeric(repl.max)
			wuhan.current.infections = numeric(repl.max)
			rest.china.infections = numeric(repl.max)
			rest.china.current.infections = numeric(repl.max)
			china.end = matrix(0, nrow=length(city.seq), ncol=repl.max)
			full.I_China = list()
			full.res_China = list()
			full.res_World = list()
			rownames(china.end) = city.seq
			pb = txtProgressBar(min=0, max=repl.max, initial=0, char="=")
			for ( repl in 1:repl.max ) {
				b = epidemic.sim( 
					beta_1=exp(rnorm(1,param$estim[1],param$se[1])), 
					gamma=exp(rnorm(1,param$estim[2],param$se[2])), 
					alpha=1/4, 
					phi=invlogit(rnorm(1,param$estim[3],param$se[3])), 
					I0W=exp(rnorm(1,param$estim[4],param$se[4])),
					t.max=t.now+t.plus,
					K1, K2
				)
				i = which(city.seq=="Wuhan")
				wuhan.infections[repl] = sum(b$I_China[i,1:T]) # this is summing the number of daily new cases
				wuhan.current.infections[repl] = b$Icurr_China[i,T]
				i = which(city.seq!="Wuhan")
				rest.china.infections[repl] = sum(b$I_China[i,1:T])
				rest.china.current.infections[repl] = sum(b$Icurr_China[i,T])
				
				# current infections at Tend -- china
				china.end[,repl] = b$Icurr_China[,Tend]
				
				# all info on new cases
				full.I_China[[repl]] = b$I_China
				full.res_China[[repl]] = b$res_China
				full.res_World[[repl]] = b$res_World
				
				setTxtProgressBar(pb,repl)
			}
			close( pb)
			round( get.mean.CI( wuhan.infections ) )
			round( get.mean.CI( wuhan.current.infections ) )
			round( get.mean.CI( rest.china.infections ) )
			round( get.mean.CI( rest.china.current.infections ) )
		
			# how big an epidemic in Wuhan do we predict for 18 Jan (t=17)
			x = stack.x(lapply(full.I_China, FUN=get.ts, name="Wuhan"))
			x2 = t(apply( x, MARGIN=1, FUN=cumsum ))
			get.mean.CI(x2[,17])
			
			# how large an epidemic in Wuhan in 14 days time?
			wuhan = stack.x(lapply(full.I_China, FUN=get.ts, name="Wuhan"))
			get.mean.CI( wuhan[,length(date.seq)] )
		
			# which countries will have the most imports?
			get.Tend = function(x) {
				x[,Tend]
			}
			x = stack.x(lapply(full.res_World, FUN=get.Tend))
			round( sort( colMeans(x), decreasing=TRUE )[1:10], 1 )
			
		# time series predictions figure
			dev.new(width=13,height=4)
				plot.time.series( a, full.I_China, full.res_World, t.now, t.plus )
			dev.copy2pdf( file="fig_projections.pdf", useDingbats=FALSE )
			dev.off()
		
		# Table 1
			x = t( apply( china.end, MARGIN=1, FUN=get.mean.CI ) )
			y = x[order(x[,1], decreasing=TRUE),]
			T1 = head(
				cbind( 
					round(y),
					round(y*phi)
				), 15
			)
			colnames( T1 ) = c("size.m","size.2.5pc","size.97.5pc","cases.m","cases.2.5pc","cases.97.5pc")
			write.csv(T1, "T1.csv")
					
		
	# effect of travel restriction to/from Wuhan
		t.now = t.max
		t.plus = 14 # take it to the start of March
		date.seq = seq( 
			from=as.Date("2020-01-01"),
			to=as.Date("2020-01-01")+t.now+t.plus,
			by=1 
		)
		dev.new(width=6,height=4)
			plot.travel.restrictions( K1, t.now, t.plus ) # now: 21 Jan
		dev.copy2pdf( file="fig_travel_restriction.pdf", useDingbats=FALSE )
		dev.off()
		

	# doubling times
		dtime = function( td, q1=1, q2 ) {
			td*(log(2)/log(q2/q1))
		}
		dtime( 22+15-1, q1=1, q2=444) # mid december start
		dtime( 21-1, q1=24, q2=11257 ) # using modelled estimates and 1 Jan start date