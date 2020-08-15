MAKE_THEME 		:= LIME

-include .env

BLACK			:= 232
LIGHTER_GREY 	:= 246
LIGHT_GREY 		:= 244
GREY		 	:= 243
DARK_GREY 		:= 237
PLAIN 			:= 255

BLUE 			:= 4
GOLD 			:= 214
LIGHTBLUE 		:= 74
LIME			:= 106
PURPLE			:= 99
PINK 			:= 219

RESET 			:= "\033[0m"
FG 				= "\033[38;5;$(1)m"
FGDIM			= "\033[2;38;5;$(1)m"
FGB				= "\033[1;38;5;$(1)m"
BG 				= "\033[48;5;$(1)m"

define print_h1
	@$(eval COLOR=$($(MAKE_THEME)))

	@if [[ -n '$(4)' ]]; \
        then printf '%b%b %s %b%b %s %b%b %s %b%b %s %b\n' $(call BG,$(DARK_GREY)) $(call FG,$(COLOR)) $(1) $(call BG,$(COLOR)) $(call FGB,$(BLACK)) $(2) $(call BG,$(DARK_GREY)) $(call FG,$(COLOR)) $(3) $(call BG,$(COLOR)) $(call FGB,$(BLACK)) $(4) $(RESET); \
	elif [[ -n '$(3)' ]]; \
        then printf '%b%b %s %b%b %s %b%b %s %b\n' $(call BG,$(DARK_GREY)) $(call FG,$(COLOR)) $(1) $(call BG,$(COLOR)) $(call FGB,$(BLACK)) $(2) $(call BG,$(DARK_GREY)) $(call FG,$(COLOR)) $(3) $(RESET); \
	elif [[ -n '$(2)' ]]; \
        then printf '%b%b %s %b%b %s %b\n' $(call BG,$(DARK_GREY)) $(call FGB,$(COLOR)) $(1) $(call BG,$(COLOR)) $(call FGB,$(BLACK)) $(2) $(RESET); \
	elif [[ -n '$(1)' ]]; \
        then printf '%b%b %s %b\n' $(call BG,$(COLOR)) $(call FGB,$(BLACK)) $(1) $(RESET); \
    fi
endef

define print_h2
	@printf '%b%b %s %b\n' $(call BG,$(LIGHT_GREY)) $(call FG,$(BLACK)) $(1) $(RESET)
endef

define print_h3
	@printf '%b %s %b\n' $(call BG,$(DARK_GREY)) $(1) $(RESET)
endef

define print
	@$(eval COLOR=$($(MAKE_THEME)))
	@printf '%b %s %b\n' $(call FG,$(COLOR)) $(1) $(RESET)
endef

define print_space
	@echo ""
endef

define print_options
	@$(eval COLOR=$($(MAKE_THEME)))
	@printf '%b %-15s %b%s%b\n' $(call FG,$(COLOR)) $(1) $(call FG,$(LIGHTER_GREY)) $(2) $(RESET)
endef

define print_warning
	@printf '%b %s %b\n' $(call FGB,$(GOLD)) $(1) $(RESET)
endef
