module Jekyll
    module BreadcrumbFilter
        def breadcrumb(input)
            crumb = '<a href="/">Home</a>'
            href = "/"
            File.dirname(input).split('/').reject {|p| p.eql? ''}.each do |p|
                href = "#{href}#{p}/"
                crumb = "#{crumb} &gt; <a href=\"#{href}\">#{p}</a>"
            end
            crumb
        end
    end
end

Liquid::Template.register_filter(Jekyll::BreadcrumbFilter)
